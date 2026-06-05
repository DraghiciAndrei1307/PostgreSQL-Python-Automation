"""
    This is the setup.py script of the os_executor module.
"""

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'This is the CLI interface between the user and the os_runner'
LONG_DESCRIPTION = ('This is a layer of abstraction that defines the way the '
                    'user should use the os_runner capabilities.')


setup(
    name='os_executor_draghici_andrei',
    version=VERSION,
    author='Andrei Draghici',
    author_email='draghici.andrei12@yahoo.com',
    url='https://github.com/draghiciandrei1307/python-automation',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'click',
        'os_runner_draghici_andrei'
    ],
    entry_points={
        'console_scripts': [
            # 'terminal command = package.file:function'
            'os_executor=os_executor.os_executor:cli',
        ],
    },
)
