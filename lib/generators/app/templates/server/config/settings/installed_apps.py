INSTALLED_APPS = (
    'constance',
    'constance.backends.database',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'adminsortable2',
    'redactor',
    'flatblocks',
    'django_redis',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'dbmail',
    'jfu',
    'corsheaders',
    'sorl.thumbnail',
    'geoposition',
    'debug_toolbar',
    'raven.contrib.django.raven_compat',
)

LOCAL_APPS = (
    # 'apps.example_app',
)

INSTALLED_APPS += LOCAL_APPS

LOCAL_MIGRATIONS = [app_path for app_path in LOCAL_APPS]

MIGRATION_PATH = '.migrations'

MIGRATION_MODULES = {
    app_name: app_name + MIGRATION_PATH
    for app_name in LOCAL_MIGRATIONS
}

