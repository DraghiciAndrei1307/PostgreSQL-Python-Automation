"""
    This module contains the os_executor logic.
"""

import click

from os_runner import OsRunner

def setup_os_runner():
    """
    Sets up the os runner.
    :return:
    """
    return OsRunner()

@click.group()
@click.pass_context
def cli(ctx):
    """
        This is a group command. We create a group for the future commands
        that we will implement in the future. In this command, we can load
        configuration files.
    """
    ctx.ensure_object(dict)

@cli.command()
@click.option('--count',
              type=int,
              default=1,
              help='Number of greetings.'
              )
@click.option('--name',
              type=str,
              prompt='Your name',
              help='The person to greet.'
              )

# @click.pass_context
# def hello(ctx, count, name):
#     """
#     Command that greets NAME for a total of COUNT times.
#     """
#     for x in range(count):
#         click.echo(f"Hello {name}!")

# @cli.command()
# @click.option('--name',
#               type=str,
#               prompt='Your name',
#               help='The person to say goodbye to.'
#               )
# @click.pass_context
# def goodbye(ctx, name):
#     """
#     Command that says goodbye NAME.
#     """
#     click.echo(f"Goodbye {name}!")

@cli.command()
@click.option(
    '--path',
    type=str,
    prompt='Enter a path',
    help='The path you want to list the entries for.'
)
@click.pass_context
def list_entries(ctx, path):
    """
        Command that lists the entries for a specific path.
    """
    os_runner = setup_os_runner()
    print(os_runner.list_entries_in_path(path=path))

@cli.command()
@click.option(
    '--path',
    type=str,
    prompt='Enter a path',
    help='The path you want to go to.'
)
@click.pass_context
def change_directory(ctx, path):
    """
        Command that changes the directory to a specific path.
    """

    os_runner = setup_os_runner()
    print(os_runner.change_current_directory(path=path))

@cli.command()
@click.option(
    '--name',
    type=str,
    prompt='How should the file be named?',
    help='The name of the file you want to create.'
)
@click.option(
    '--path',
    type=str,
    prompt='Enter a path',
    help='The path where you want to create the new file.'
)
@click.option(
    '--mode',
    type=str,
    prompt='Configure the mode of the file.',
    help='The mode of the file. Use digits to configure the mode (e.g. 0644).'
)
@click.pass_context
def create_file(ctx, name, path, mode):
    """
    Command that creates a new file.
    :param ctx:
    :param name:
    :param path:
    :param mode:
    :return:
    """
    os_runner = setup_os_runner()
    print(os_runner.create_file(name=name, path=path, mode=mode))

@cli.command()
@click.option(
    '--path',
    type=str,
    prompt='Enter a path',
    help='The path you want to change the mode for.'
)
@click.option(
    '--mode',
    type=str,
    prompt='Mode',
    help='The mode you want to change to.'
)
@click.pass_context
def change_access_rights(ctx, path, mode):
    """
    Command that changes the access rights of the path.
    :param ctx:
    :param path:
    :param mode:
    :return:
    """
    os_runner = setup_os_runner()
    print(os_runner.change_mode(path, mode))

@cli.command()
@click.option(
    '--path',
    type=str,
    prompt='Enter a path',
    help='The path you want to create the new folder.'
)
@click.option(
    '--name',
    type=str,
    prompt='How should the folder be named?',
    help='The name of the folder you want to create.'
)
@click.option(
    '--mode',
    type=str,
    prompt='Mode',
    help='The mode you want to change to. '
         'Use digits to configure the mode (e.g. 0644).'
)
@click.pass_context
def create_folder(ctx, path, name, mode):
    """
    Command that creates a new folder.
    :param ctx:
    :param path:
    :param name:
    :param mode:
    :return:
    """
    os_runner = setup_os_runner()
    print(os_runner.create_folder(path=path, name=name, mode=mode))

@cli.command()
@click.option(
    '--src',
    type=str,
    prompt='Enter a source path',
    help='The source path you want to copy from.'
)
@click.option(
    '--dest',
    type=str,
    prompt='Enter a destination path',
    help='The destination path you want to copy to.'
)
@click.pass_context
def move(ctx, src, dest):
    """
    Command that moves files from src to dest.
    :param ctx:
    :param src:
    :param dest:
    :return:
    """
    os_runner = setup_os_runner()
    print(os_runner.move(source=src, destination=dest))

@cli.command(name="run-command")
@click.option(
    '--command',
    type=str,
    prompt='Enter a command',
    help='The command you want to run.',
)
@click.pass_context
def run_cmd(ctx, command):
    """
    Command that runs a command.
    :param ctx:
    :param command:
    :return:
    """
    if not command:
        click.echo("Error: You need to enter a command.")
        return

    os_runner = setup_os_runner()
    print(os_runner.run_cmd(command))
