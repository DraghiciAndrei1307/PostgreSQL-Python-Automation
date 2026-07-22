"""
    Here we define the BackupScheduler class which
    uses the Celery Beat scheduler to schedule the
    execution of the 'perform_backup' task.
"""


from .tasks import perform_backup

from django_celery_beat.models import (
    ClockedSchedule,
    PeriodicTask
)

import json

class BackupScheduler:

    def schedule(self, instance_id, schedule_at):
        # create the schedule for the Celery Beat
        # we will use perform_backup task here
        clocked, _ = ClockedSchedule.objects.get_or_create(
            clocked_time=schedule_at,
        )

        PeriodicTask.objects.create(
            name=f"backup-{instance_id}",
            task="provisioner_api.tasks.perform_backup",
            clocked=clocked,
            one_off=True,
            args=json.dumps([instance_id])
        )
