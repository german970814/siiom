from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, hosts
import random

REPO_URL = 'https://taniamhn@bitbucket.org/ingeniarte/iglesia.git'

env.hosts = ['iglesia.webfactional.com', 'panama.iglesia.webfactional.com',
            'gng.iglesia.webfactional.com', 'cdo.iglesia.webfactional.com']
env.user = 'iglesia'

enviroments = {
    'siiom.conial.net': {
        'name': 'siiom',
        'db': 'siiom',
        'user': 'siiom',
        'pass': '123456',
        'source': 'develop'
    },

    'iglesia.webfactional.com': {
        'name': 'cdr',
        'db': 'iglesia_prod',
        'user': 'iglesia',
        'pass': 'ecbddac9',
        'source': 'master'
    },

    'panama.iglesia.webfactional.com': {
        'name': 'vps',
        'db': 'panama_prod',
        'user': 'iglesia',
        'pass': 'ecbddac9',
        'source': 'master'
    },

    'gng.iglesia.webfactional.com': {
        'name': 'gng',
        'db': 'gng',
        'user': 'iglesia',
        'pass': 'ecbddac9',
        'source': 'master'
    },

    'cdo.iglesia.webfactional.com': {
        'name': 'cdo',
        'db': 'cdo',
        'user': 'iglesia',
        'pass': 'ecbddac9',
        'source': 'master'
    }
}


@hosts('conial@siiom.conial.net')
def staging():
    deploy()


def deploy():
    site_folder = '/home/%s/webapps/siiom/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(env.user, env.host, source_folder)
    _update_static_files(source_folder, env.user, env.host)
    _update_database_info(source_folder, env.host)
    _update_database(source_folder, env.user, env.host)
    _restart_gunicorn_server(env.user, env.host)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('static', 'source', 'media'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))

    source = enviroments[env.host]['source']

    current_commit = local("git log origin/" + source + " -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/Iglesia/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
        )

    secret_key_file = source_folder + '/Iglesia/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(user, site_name, source_folder):
    virtualenv_folder = '/home/%s/.envs/%s' % (user, site_name)
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
        run('%s/bin/pip install newrelic' % (virtualenv_folder,))

    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder, user, site_name):
    run('cd %s && /home/%s/.envs/%s/bin/python3 manage.py collectstatic --noinput' % (
        source_folder, user, site_name
    ))


def _update_database_info(source_folder, host):
    database_path = source_folder + '/Iglesia/database.py'

    valores = enviroments[host]
    sed(database_path, 'NAME = ""', 'NAME = "%s"' % (valores['db']))
    sed(database_path, 'USER = ""', 'USER = "%s"' % (valores['user']))
    sed(database_path, 'PASSWORD = ""', 'PASSWORD = "%s"' % (valores['pass']))


def _update_database(source_folder, user, site_name):
    run('cd %s && /home/%s/.envs/%s/bin/python3 manage.py migrate --noinput' % (
        source_folder, user, site_name
    ))


def _restart_gunicorn_server(user, host):
    name = enviroments[host]['name']
    run('/home/%s/bin/supervisorctl -c /home/%s/etc/supervisord.conf restart %s' % (user, user, name))
    run('/home/%s/bin/supervisorctl -c /home/%s/etc/supervisord.conf status %s' % (user, user, name))
