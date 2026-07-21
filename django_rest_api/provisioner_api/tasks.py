"""
    This module contains the task definitions. Tasks
    executed by the Celery worker.
"""

import os
import django
from celery import Celery
from django.conf import settings

from pg_provisioner import PgProvisioner

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_config.settings')
django.setup()

from .models import PostgreSQLVM, PostgreSQLBackup

app = Celery('django_rest_api', broker='redis://localhost:6379/0')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task
def run_ansible_provisioning_task(instance_id):
    """
        This is the function represents the task
        executed by the Celery worker. Notice the
        '@app.task' decorator.
    """

    try:
        vm = PostgreSQLVM.objects.get(id=instance_id)
    except PostgreSQLVM.DoesNotExist:
        return "VM not found"

    vm.status = "Provisioning"
    vm.save()

    provisioner = PgProvisioner()

    result = provisioner.start_pg_vm_provisioning(
        name=vm.vm_name,
        base=vm.base_vm_name,
        vm_id=instance_id
    )

    if result['success']:
        vm.status = "Ready"
    else:
        vm.status = "Failed"

    vm.save(update_fields=['status'])
    return (
        f"Provisioning finished for {vm.vm_name} with status {vm.status}.\n"
        f"RESULT: \n"
        f"{result}"
    )

@app.task(bind=True)
def perform_backup(instance_id):
    """
        This is yet another task that deals with
        the full backup right after the provisioning was
        performed.
    """

    try:
        backup = PostgreSQLBackup.objects.get(id=instance_id)
    except PostgreSQLBackup.DoesNotExist:
        return "Backup not found"

    backup.status = "In Progress"
    backup.save()

    provisioner = PgProvisioner()

    cluster = backup.instance

    result = provisioner.perform_full_backup(instance_name=cluster.vm.vm_name, backup_id=instance_id)

    print(result)

    if result['success']:
        backup.status = "Finished"
    else:
        backup.status = "Failed"

    # this needs adjustment with the actual fields that need to be updated

    backup.save(update_fields=['status'])

    return f"Full backup performed for the {str(cluster)}"
