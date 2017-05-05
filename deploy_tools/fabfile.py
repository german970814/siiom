import random
from contextlib import contextmanager
from fabric.contrib.files import append, sed
from fabric.api import env, task, run, sudo, cd, prefix, local

REPO_URL = 'git@bitbucket.org:ingeniarte/siiom.git'
# psql -U siiom -h localhost siiom < ~/Desktop/staging_tenant.sql
# rsync -nrv --exclude=.DS_Store . ingeniarte@staging.siiom.net:/home/ingeniarte/sites/ingeniarte.siiom.net/media/cdr.siiom.net/
# return 301 $scheme://tenant.staging.siiom.net$request_uri;
# sudo certbot certonly --cert-name staging.siiom.net --webroot -w /home/ingeniarte/sites/staging.siiom.net -d staging.siiom.net -d tenant.staging.siiom.net -d gng.staging.siiom.net

ENVIROMENT_SETTINGS = {
    'production': {
        'site': 'ingeniarte.siiom.net',
        'branch': 'master',
        'allowed_host': '.siiom.net',
        'db': {
            'name': 'siiom',
            'pass': 'dbsiiom2017',
            'user': 'siiom'
        }
    },
    'staging': {
        'site': 'staging.siiom.net',
        'branch': 'develop',
        'allowed_host': '.staging.siiom.net',
        'db': {
            'name': 'siiom_staging',
            'pass': 'dbsiiom2017',
            'user': 'siiom'
        }
    }
}


def site_dir():
    global SITE_FOLDER, PROJECT_ROOT
    env.site = env.settings['site']
    SITE_FOLDER = '/home/{user}/sites/{site}'.format(user=env.user, site=env.site)
    PROJECT_ROOT = '{}/src'.format(SITE_FOLDER)


@contextmanager
def virtualenv():
    with prefix('workon {}'.format(env.site)):
        yield


def create_secret_key():
    secret_key_file = PROJECT_ROOT + '/siiom/secret_key.py'
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    append(secret_key_file, "SECRET_KEY = '{}'".format(key))


def update_settings():
    # settings_path = PROJECT_ROOT + '/siiom/settings.py'
    settings_path = PROJECT_ROOT + '/siiom/settings/production.py'
    # sed(settings_path, "DEBUG = True", "DEBUG = False")
    # sed(settings_path,
    #     'ALLOWED_HOSTS =.+$',
    #     'ALLOWED_HOSTS = ["{}"]'.format(env.settings['allowed_host'])
    #     )
    append(settings_path, '\nALLOWED_HOSTS = ["{}"]'.format(env.settings['allowed_host']))
    append(settings_path, '\nfrom ..secret_key import SECRET_KEY')


def update_database():
    database_path = PROJECT_ROOT + '/siiom/database.py'
    db_settings = env.settings['db']

    sed(database_path, 'NAME = ""', 'NAME = "%s"' % (db_settings['name']))
    sed(database_path, 'USER = ""', 'USER = "%s"' % (db_settings['user']))
    sed(database_path, 'PASSWORD = ""', 'PASSWORD = "%s"' % (db_settings['pass']))


def update_source():
    commit = local('git rev-parse origin/{}'.format(env.settings['branch']), capture=True)

    with virtualenv():
        run('git fetch')
        run('git reset --hard {}'.format(commit))


def config_gunicorn():
    file_ = 'gunicorn_start'
    with cd('{}/bin'.format(SITE_FOLDER)):
        sudo('cp {}/deploy_tools/gunicorn.template.conf {}'.format(PROJECT_ROOT, file_))
        sed(file_, 'PROJECT_ROOT', PROJECT_ROOT)
        sed(file_, 'SITE_FOLDER', SITE_FOLDER)
        sed(file_, 'SITENAME', env.site)
        sed(file_, 'USER', env.user)

        run('chmod u+x {}'.format(file_))


def config_services():
    CONFIG_FILES = {
        'supervisor': 'conf.d/{}.conf'.format(env.site),
        'nginx': 'sites-available/{}.conf'.format(env.site)
    }

    for service in ('nginx', 'supervisor'):
        with cd('/etc/{}/'.format(service)):
            sudo('cp {}/deploy_tools/{}.template.conf {}'.format(PROJECT_ROOT, service, CONFIG_FILES[service]))
            sed(CONFIG_FILES[service], 'HOSTNAME', env.settings['allowed_host'], use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'PROJECT_ROOT', PROJECT_ROOT, use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'SITE_FOLDER', SITE_FOLDER, use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'SITENAME', env.site, use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'USER', env.user, use_sudo=True, shell=True)

    sudo('ln -s {nginx}/{} {nginx}/sites-enabled'.format(CONFIG_FILES['nginx'], env.site, nginx='/etc/nginx'))
    config_gunicorn()


@task
def staging():
    """Setting staging enviroment."""

    env.user = 'ingeniarte'
    env.hosts = ['staging.siiom.net']
    env.settings = ENVIROMENT_SETTINGS['staging']

    site_dir()


@task
def production():
    """Setting production enviroment."""

    env.user = 'ingeniarte'
    env.hosts = ['ingeniarte.siiom.net']
    env.settings = ENVIROMENT_SETTINGS['production']

    site_dir()


@task
def provision():
    """Provision a new site on an already provision server."""

    for subfolder in ('static', 'media', 'src', 'bin', 'tmp/sockets', 'tmp/logs'):
        run("mkdir -p {}/{}".format(SITE_FOLDER, subfolder))

    run('git clone {} {}'.format(REPO_URL, PROJECT_ROOT))

    #  Create virtualenv
    run('mkvirtualenv {}'.format(env.site))
    with cd(PROJECT_ROOT):
        with virtualenv():
            run('setvirtualenvproject')

    update_source()
    create_secret_key()
    update_database()
    update_settings()
    with virtualenv():
        run('pip install -r requirements/production.txt')
        run('./manage.py migrate_schemas --shared')
        run('./manage.py collectstatic --noinput')

    config_services()

    sudo('systemctl reload nginx')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


@task
def deploy():
    """Deploy new changes to the server."""

    update_source()
    update_settings()
    update_database()
    with virtualenv():
        run('pip install -r requirements/production.txt')
        run('./manage.py migrate_schemas')
        run('./manage.py collectstatic --noinput')

    sudo('supervisorctl restart {}'.format(env.site))
    sudo('supervisorctl status {}'.format(env.site))
