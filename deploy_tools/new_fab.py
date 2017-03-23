import random
from contextlib import contextmanager
from fabric.contrib.files import append, sed
from fabric.api import env, task, run, sudo, cd, prefix, local

REPO_URL = 'git@bitbucket.org:ingeniarte/siiom.git'

SITE_FOLDER = '/home/{user}/sites/{site}'.format(user=env.user, site=env.host)
PROJECT_ROOT = '{}/src'.format(SITE_FOLDER)

ENVIROMENT_SETTINGS = {
    'production': {
        'branch': 'master',
        'allowed_host': '*.siiom.net',
        'db': {
            'name': 'siiom',
            'pass': 'dbsiiom2017',
            'user': 'siiom'
        }
    },
    'staging': {
        'branch': 'tenant',
        'allowed_host': 'staging.siiom.net',
        'db': {
            'name': 'siiom_staging',
            'pass': 'dbsiiom2017',
            'user': 'siiom'
        }
    }
}


@contextmanager
def virtualenv():
    with prefix('workon {}'.format(env.host)):
        yield


def create_secret_key():
    secret_key_file = PROJECT_ROOT + '/Iglesia/secret_key.py'
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    append(secret_key_file, "SECRET_KEY = '{}'".format(key))


def update_settings():
    settings_path = PROJECT_ROOT + '/Iglesia/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{}"]'.format(env.settings['allowed_host'])
        )

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def update_database():
    database_path = PROJECT_ROOT + '/Iglesia/database.py'
    db_settings = env.settings['db']

    sed(database_path, 'NAME = ""', 'NAME = "%s"' % (db_settings['name']))
    sed(database_path, 'USER = ""', 'USER = "%s"' % (db_settings['user']))
    sed(database_path, 'PASSWORD = ""', 'PASSWORD = "%s"' % (db_settings['pass']))


def update_source():
    run('git fetch')
    commit = local('git log origin2/{} -n 1 --format=%H'.format(env.settings['branch'], capture=True))
    run('git reset --hard {}'.format(commit))


def config_services():
    CONFIG_FILES = {
        'gunicorn': '{}_start'.format(env.host),
        'supervisor': 'conf.d/{}.conf'.format(env.host),
        'nginx': 'sites-available/{}.conf'.format(env.host)
    }

    for service in ('nginx', 'gunicorn', 'supervisor'):
        with cd('/etc/{}/'.format(service)):
            sudo('cp {}/deploy_tools/{}.template.conf {}'.format(PROJECT_ROOT, service, CONFIG_FILES[service]))
            sudo(sed(CONFIG_FILES[service], 'SITENAME', env.host))
            sudo(sed(CONFIG_FILES[service], 'SITE_FOLDER', SITE_FOLDER))
            sudo(sed(CONFIG_FILES[service], 'HOSTNAME', env.settings['allowed_host']))

    sudo('chmod u+x /etc/gunicorn/{}'.format(CONFIG_FILES['gunicorn']))
    sudo('ln -s {nging}/{} {nginx}/sites-enabled'.format(CONFIG_FILES['nginx'], env.host, nginx='/etc/nginx'))


@task
def staging():
    """Setting staging enviroment."""

    env.hosts = ['ingeniarte@staging.siiom.net']
    env.settings = ENVIROMENT_SETTINGS['staging']


@task
def production():
    """Setting production enviroment."""

    env.hosts = ['ingeniarte@ingeniarte.siiom.net']
    env.settings = ENVIROMENT_SETTINGS['staging']


@task
def provision():
    """Provision a new site on an already provision server."""

    for subfolder in ('static, media, src, tmp/sockets tmp/logs'):
        run("mkdir -p {}/{}".format(SITE_FOLDER, subfolder))

    run('git clone {} {}'.format(REPO_URL, PROJECT_ROOT))

    #  Create virtualenv
    run('mkvirtualenv {}'.format(env.host))
    with cd(PROJECT_ROOT):
        with virtualenv():
            run('setvirtualenvproject')

    with virtualenv():
        update_source()
        create_secret_key()
        update_database()
        update_settings()
        run('pip install -r requirements/production.txt')
        run('./manage.py migrate_schemas --shared')
        run('./manage.py collectstatic')

    config_services()

    sudo('systemctl reload nginx')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


@task
def deploy():
    """Deploy new changes to the server"""

    with virtualenv:
        update_source()
        update_settings()
        update_database()
        run('pip install -r requirements/production.txt')
        run('./manage.py migrate_schemas')
        run('./manage.py collectstatic')

    sudo('supervisorctl restart {}'.format(env.host))
    sudo('supervisorctl status {}'.format(env.host))
