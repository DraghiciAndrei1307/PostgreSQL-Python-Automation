"""
This module acts as a CLI interface for pg_provisioner.
"""
import click
from pg_provisioner import PgProvisioner


def setup_pg_provisioner():
    """
    Sets up the pg provisioner.
    :return:
    """
    return PgProvisioner()


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
@click.pass_context
def provision_new_pg_vm(ctx):
    """
        Method that uses the pg_provisioner to start
        the PostgreSQL VM provisioning process.
    """

    print("DEBUG: Start provisioning command...")
    try:
        pg_provisioner = setup_pg_provisioner()
        print(
            f"DEBUG: PgProvisioner instantiated. "
            f"Vault pass set: "
            f"{bool(pg_provisioner.vault_password)}"
        )
        pg_provisioner.start_pg_vm_provisioning(
            name='test',
            base='bronze',
            vm_id='1'
        )
        print("DEBUG: Command sent to OsRunner.")
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
