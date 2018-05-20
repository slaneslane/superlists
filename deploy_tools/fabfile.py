import os
import random
from fabric.contrib.files import append, exists, sed
from fabric.api import cd, env, local, run, sudo

REPO_URL = 'https://github.com/slaneslane/superlists.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtual_env()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

    _update_and_copy_ngingx_conf_file(site_folder)
    _link_ngingx_conf_file()
    _update_and_copy_systemd_conf_file(site_folder)
    _reload_all_services()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtual_env():
    if not exists('virtualenv/bin/pip'):
        run('python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret_key = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        append('.env', f'DJANGO_SECRET_KEY={new_secret_key}')

def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')
    
def _update_and_copy_ngingx_conf_file(site_folder):
    SITE_AVAILABLE_PATH = f'/etc/nginx/sites-available/{env.host}'
    with cd(os.path.join(site_folder, 'deploy_tools')):
        sed('nginx.template.conf', 'DOMAIN', env.host, backup='')
        sudo(f'cp nginx.template.conf {SITE_AVAILABLE_PATH}')

def _link_ngingx_conf_file():
    SITE_AVAILABLE_PATH = f'/etc/nginx/sites-available/{env.host}'
    SITE_ENABLED_PATH = f'/etc/nginx/sites-enabled/{env.host}'
    if not exists(SITE_ENABLED_PATH):
        sudo(f'ln -s {SITE_AVAILABLE_PATH} {SITE_ENABLED_PATH}')
    run(f'cat {SITE_ENABLED_PATH}')

def _update_and_copy_systemd_conf_file(site_folder):
    SERVICE_TEMPLATE = 'gunicorn-systemd.template.service'
    SERVICE_PATH = f'/etc/systemd/system/gunicorn-{env.host}.service'
    with cd(os.path.join(site_folder, 'deploy_tools')):
        sed(SERVICE_TEMPLATE, 'DOMAIN', env.host, backup='')
        sudo(f'cp {SERVICE_TEMPLATE} {SERVICE_PATH}') 
        run(f'cat {SERVICE_PATH}')

def _reload_all_services():
    SERVICE_PATH = f'/etc/systemd/system/gunicorn-{env.host}.service'
    sudo('systemctl daemon-reload')
    sudo('systemctl reload nginx')
    sudo(f'systemctl enable gunicorn-{env.host}')
    sudo(f'systemctl start gunicorn-{env.host}')
