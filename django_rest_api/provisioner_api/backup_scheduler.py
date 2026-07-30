"""
    Here we define the BackupScheduler class which
    uses the Celery Beat scheduler to schedule the
    execution of the 'perform_backup' task.
"""
from .models import PostgreSQLBackup, BackupSchedule
from .tasks import perform_backup

from django_celery_beat.models import (
    ClockedSchedule,
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
)

from datetime import timedelta

import json

class BackupScheduler:

    def schedule(self, backup):
        if backup.schedule.schedule_type == BackupSchedule.ScheduleType.IMMEDIATE:
            perform_backup.delay(backup.id)
        elif backup.schedule.schedule_type == BackupSchedule.ScheduleType.ONCE:
            self.schedule_once(instance_id=backup.id, schedule_at=backup.schedule.execute_at)
        elif backup.schedule.schedule_type == BackupSchedule.ScheduleType.INTERVAL:
            self.schedule_interval(instance_id=backup.id, every=backup.schedule.every, period=backup.schedule.period)
        elif backup.schedule.schedule_type == BackupSchedule.ScheduleType.CRON:
            self.schedule_cron(backup.id, backup.schedule.cron)
        elif backup.schedule.schedule_type == BackupSchedule.ScheduleType.BENCHMARK:
            self.schedule_benchmark_test(backup.id, number_of_iterations=1000, start_at=backup.schedule.execute_at)

    def schedule_once(self, instance_id, schedule_at):
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

    def schedule_interval(self, instance_id, every, period):
        interval, _ = IntervalSchedule.objects.get_or_create(
            every=every,
            period=period.lower(),
        )

        PeriodicTask.objects.create(
            name=f"backup-{instance_id}",
            task="provisioner_api.tasks.perform_backup",
            interval=interval,
            args=json.dumps([instance_id]),
        )

    def schedule_cron(self, instance_id, cron):
        minute, hour, day_of_month, month_of_year, day_of_week = cron.split()

        crontab, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            day_of_week=day_of_week,
        )

        PeriodicTask.objects.create(
            name=f"backup-{instance_id}",
            task="provisioner_api.tasks.perform_backup",
            crontab=crontab,
            args=json.dumps([instance_id]),
        )

    def schedule_benchmark_test(self, instance_id, number_of_iterations, start_at):

        for i in range(number_of_iterations):

            # create the schedule for the Celery Beat
            # we will use perform_backup task here
            clocked, _ = ClockedSchedule.objects.get_or_create(
                clocked_time=start_at + timedelta(seconds=i*10),
            )

            PeriodicTask.objects.create(
                name=f"backup-{instance_id}-{i}",
                task="provisioner_api.tasks.perform_backup",
                clocked=clocked,
                one_off=True,
                args=json.dumps([instance_id])
            )

