from fabric.api import local


def restore_backup(path):
    if '.dump' in path:
        binary = 'True'
    elif '.sql' in path:
        binary = 'False'
    elif path == '':
        return

    if binary == 'True':
        cmd = "docker exec -i $(docker ps | grep db_ | awk '{{ print $1 }}') pg_restore --no-acl --no-owner -U postgres -d postgres < {0}".format(path)
    else:
        cmd = "docker exec -i $(docker ps | grep db_ | awk '{{ print $1 }}') psql -U postgres -d postgres < {0}".format(path)

    local(cmd)


def migrate(app=''):
    local("docker exec -i $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py migrate {}".format(app))


def createsuperuser():
    local("docker exec -it $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py createsuperuser")


def stop():
    local('docker-compose kill')


def start():
    local('docker-compose up')


def restart():
    local('docker-compose kill')
    local('docker-compose up')


def makemigrations(app=''):
    local("docker exec -i $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py makemigrations {}".format(app))


def initialize(dump_path=''):
    restore_backup(dump_path)
    migrate()
    createsuperuser()
    restart()


def ci(test_args=''):
    test_arg = 'test_args={};'.format(test_args) if test_args else ''
    local('cd server && fab ci:test_args={}'.format(test_arg))


def test(coverage=None, test_args=''):
    cov_arg = 'coverage={};'.format(coverage) if coverage else ''
    test_arg = 'test_args={};'.format(test_args) if test_args else ''
    local('cd server && fab test:{}{}'.format(cov_arg, test_arg))


def bash():
    local("docker exec -it $(docker ps | grep server_ | awk '{{ print $1 }}') bash")


def shell():
    local("docker exec -it $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py shell")

