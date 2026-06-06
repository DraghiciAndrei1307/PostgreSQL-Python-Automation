"""
This module acts as a CLI interface for pg_runner.
"""
import click

from pg_runner import PgRunner

# ------------------ PgRunner functions ------------------------ #


def setup_pg_runner():
    """
    Sets up the pg runner.
    :return:
    """
    return PgRunner()


@click.group()
@click.pass_context
def cli(ctx):
    """
    This is a group command. We create a group for the future commands
    that we will implement in the future. In this command, we can load
     configuration files.
    :param ctx:
    :return:
    """
    ctx.ensure_object(dict)


@cli.command()
@click.option(
    '--version',
    type=int,
    default=14,
    help='PostgreSQL version.'
)
@click.pass_context
def check_postgresql_status(ctx, version):
    """
    Method that checks if the database is up and running or not.
    :param ctx:
    :param version:
    :return:
    """

    pg_runner = setup_pg_runner()
    pg_runner.check_postgresql_status(version=version)


@cli.command()
@click.option(
    '--version',
    type=int,
    default=14,
    help='PostgreSQL version.'
)
@click.pass_context
def start_pg(ctx, version):
    """
    Method that uses the pg_runner
    to start the cluster.
    :param ctx:
    :param version:
    :return:
    """
    pg_runner = setup_pg_runner()
    pg_runner.start_pg(version=version)


@cli.command()
@click.option(
    '--version',
    type=int,
    default=14,
    help='PostgreSQL version.'
)
@click.pass_context
def stop_pg(ctx, version):
    """
    Method that uses the pg_runner
    to stop the cluster.
    :param ctx:
    :param version:
    :return:
    """
    pg_runner = setup_pg_runner()
    pg_runner.stop_pg(version=version)


@cli.command()
@click.pass_context
def backup_pg(ctx):
    """
    Method that uses the pg_runner
    to backup the database.
    :param ctx:
    :return:
    """
    pg_runner = setup_pg_runner()
    pg_runner.backup_pg()


@cli.command()
@click.pass_context
def backup_info(ctx):
    """
    Method that uses the pg_runner
    to check the backup history.
    :param ctx:
    :return:
    """
    pg_runner = setup_pg_runner()
    pg_runner.backup_info()


@cli.command()
@click.pass_context
def check_stanza(ctx):
    """
    Method that checks the
    pgBackRest stanza.
    :param ctx:
    :return:
    """
    pg_runner = setup_pg_runner()
    pg_runner.check_stanza()

# -------------------------------------------------------------- #
