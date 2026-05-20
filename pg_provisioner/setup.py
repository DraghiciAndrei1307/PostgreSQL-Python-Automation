"""
This package acts as a layer of
abstraction (a CLI interface)
between the Django API and the Ansible provisioning platform.
"""

from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'This is the pg_provisioner module.'
LONG_DESCRIPTION = (
    'This is the CLI interface that stands '
    'between the Django API and the Ansible provisioning platform.'
)
AUTHOR = 'Andrei Draghici'
AUTHOR_EMAIL = 'draghici.andrei12@yahoo.com'

setup(
    name='pg_provisioner_draghici_andrei',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Andrei Draghici',
    author_email='draghici.andrei12@yahoo.com',
    url='https://github.com/draghiciandrei1307/python-automation',
    packages=find_packages(),
    install_requires=[
        'os_runner_draghici_andrei'
    ]

)





