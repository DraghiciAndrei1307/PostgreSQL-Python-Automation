from django.db import models

from .postgres import (
    PostgreSQLInstance,
    BackupSchedule,
    PostgreSQLBackup
)

class Order(models.Model):

    class Actions(models.TextChoices):
        """
        Actions class.
        """

        PROVISION = ('PROVISION', 'provision')
        BACKUP = ('BACKUP', 'backup')
        RESTORE = ('RESTORE', 'restore')
        DELETE = ('DELETE', 'delete')

    class Resources(models.TextChoices):
        """
        Resources class.
        """

        POSTGRESQLVM = ('POSTGRESQLVM', 'postgresqlvm')

    class Status(models.TextChoices):
        """
        Status class.
        """

        QUEUED = ('QUEUED', 'queued')
        IN_PROGRESS = ('IN PROGRESS', 'in progress')
        COMPLETED = ('COMPLETED', 'completed')
        FAILED = ('FAILED', 'failed')

    action_to_perform = models.CharField(
        choices=Actions.choices,
        default=Actions.PROVISION,
        max_length=200
    )

    resource = models.CharField(
        choices=Resources.choices,
        default=Resources.POSTGRESQLVM,
        max_length=200
    )

    status = models.CharField(
        choices=Status.choices,
        default=Status.QUEUED,
        max_length=200
    )

# ACTIONS PARAMETERS CLASSES

class ProvisionParameters(models.Model):

    class BaseVMName(models.TextChoices):
        BRONZE = ('BRONZE', 'bronze')
        SILVER = ('SILVER', 'silver')
        GOLD = ('GOLD', 'gold')

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='provision_parameters',
    )

    name=models.CharField(max_length=200, default='')

    base_vm_name=models.CharField(
        choices=BaseVMName.choices,
        default=BaseVMName.BRONZE,
        max_length=200
    )

class BackupParameters(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='backup_parameters',
    )

    backup_type=models.CharField(
        choices=PostgreSQLBackup.BackupType.choices,
        default=PostgreSQLBackup.BackupType.FULL,
        max_length=200
    )

    schedule_type = models.CharField(
        choices=BackupSchedule.ScheduleType.choices,
        default=BackupSchedule.ScheduleType.IMMEDIATE,
        max_length=200
    )

    execute_at = models.DateTimeField(
        null=True,
        blank=True
    )

    every = models.IntegerField(
        null=True,
        blank=True
    )

    period = models.CharField(
        max_length=20,
        choices=Period.choices,
    )

    # for schedule_type = "CRON"

    cron = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    instance=models.ForeignKey(
        PostgreSQLInstance,
        on_delete=models.CASCADE,
    )

class RestoreParameters(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='restore_parameters',
    )

class DeleteParameters(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delete_parameters',
    )

