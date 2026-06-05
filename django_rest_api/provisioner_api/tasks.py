"""
    This module contains the task definitions. Tasks
    executed by the Celery worker.
"""

import os
import django
from celery import Celery

from pg_provisioner import PgProvisioner

from .models import PostgreSQLVM

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_config.settings')
django.setup()

app = Celery('provisioner', broker='redis://localhost:6379/0')




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
    return f"Provisioning finished for {vm.vm_name} with status {vm.status}."
