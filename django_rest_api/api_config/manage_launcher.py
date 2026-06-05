"""
    This module defines the functions
    used for creating the entrypoints
    of this package.
"""

import os
import sys
import argparse
import django


def setup_django():
    """
        This function creates an environment variable
        that points to the settings.py of this package.
    """

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_config.settings')
    django.setup()


def main():
    """
        This defines the main entry point that we use to
        run the Django server.
    """

    setup_django()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django is not installed") from exc

    # no args: the server will start on 0.0.0.0:9001
    args = sys.argv
    if len(args) == 1:
        args.append('runserver')
        args.append('0.0.0.0:9001')

    execute_from_command_line(args)


def create_superuser():
    """
        This function is used for creating a superuser.
    """

    setup_django()

    try:
        from django.contrib.auth import get_user_model
    except ImportError as exc:
        raise ImportError("Django is not installed") from exc

    user = get_user_model()

    parser = argparse.ArgumentParser(description='Create Django superuser')
    parser.add_argument(
        '-u',
        '--username',
        required=True,
        help='Username',
        default=os.environ.get(
            'DJANGO_SUPERUSER_NAME',
            'admin'
        )
    )
    parser.add_argument(
        '-e',
        '--email',
        required=True,
        help='Email',
        default=os.environ.get(
            'DJANGO_SUPERUSER_EMAIL',
            'admin@example.com'
        )
    )
    parser.add_argument(
        '-p',
        '--password',
        required=True,
        help='Password',
        default=os.environ.get(
            'DJANGO_SUPERUSER_PASSWORD',
            'password123'
        )
    )

    args = parser.parse_args()

    if not user.objects.filter(username=args.username).exists():
        user.objects.create_superuser(args.username, args.email, args.password)
        print(f"Superuser {args.username} was created.")
    else:
        print("Your superuser already exists.")


def create_user():

    """
        This function is used for creating a normal user.
    """

    setup_django()

    try:
        from django.contrib.auth import get_user_model
    except ImportError as exc:
        raise ImportError("Django is not installed") from exc

    user = get_user_model()

    parser = argparse.ArgumentParser(
        description='Create Django superuser'
    )
    parser.add_argument(
        '-u',
        '--username',
        required=True,
        help='Username',
        default='neo'
    )
    parser.add_argument(
        '-e',
        '--email',
        required=True,
        help='Email',
        default='neo@example.com'
    )
    parser.add_argument(
        '-p',
        '--password',
        required=True,
        help='Password',
        default='password123'
    )

    args = parser.parse_args()

    if not user.objects.filter(username=args.username).exists():
        user.objects.create_user(args.username, args.email, args.password)
        print(f"User {args.username} was created.")
    else:
        print("User already exists.")
