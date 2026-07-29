"""
This package acts as a layer of
abstraction (an API interface)
between the user and the pg_provisioner_cli module.

This package must be executed on the master node.

"""

from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'This is the django_rest_api module.'
LONG_DESCRIPTION = (
    'This is the CLI interface that stands '
    'between module the user and the pg_runner.'
)
AUTHOR = 'Andrei Draghici'
AUTHOR_EMAIL = 'draghici.andrei12@yahoo.com'

setup(
    name='django_rest_api_draghici_andrei',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Andrei Draghici',
    author_email='draghici.andrei12@yahoo.com',
    url='https://github.com/draghiciandrei1307/python-automation',
    packages=find_packages(),
    install_requires=[
        'click',
        'psutil',
        'pg_provisioner_draghici_andrei',
        'djangorestframework',
        'django-celery-beat'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run-pg-api='
            'django_api.manage_launcher:main',
            'pg-api-create-superuser='
            'django_api.manage_launcher:create_superuser',
            'pg-api-create-user='
            'django_api.manage_launcher:create_user',
            'migrate-pg-api='
            'django.core.management:execute_from_command_line'
        ]
    }

)
