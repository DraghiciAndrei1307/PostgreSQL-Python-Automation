import os
import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_config.settings')
django.setup()

app = Celery('provisioner', broker='redis://localhost:6379/0')

from pg_provisioner import PgProvisioner
from .models import PostgreSQLVM

@app.task
def run_ansible_provisioning_task(instance_id):

    try:
        vm = PostgreSQLVM.objects.get(id=instance_id)
    except PostgreSQLVM.DoesNotExist:
        return "VM not found"

    vm.status = "Provisioning"
    vm.save()

    provisioner = PgProvisioner()

    result = provisioner.start_pg_vm_provisioning(name=vm.name, vm_id=instance_id)

    if result['success']:
        vm.status = "Ready"
    else:
        vm.status = "Failed"

    vm.save()
    return f"Provisioning finished for {vm.name} with status {vm.status}."