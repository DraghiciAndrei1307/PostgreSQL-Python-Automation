"""
    In this module we define our models.
"""
from datetime import datetime
from django.utils import timezone

from django.db import models
from django.core.exceptions import ValidationError


class PostgreSQLVM(models.Model):

    """ Represents a VM provisioned with PostgreSQL."""

    # ATTRIBUTES

    vm_name = models.CharField(max_length=200, default='')
    base_vm_name = models.CharField(max_length=200, default='')
    ipv4_address = models.GenericIPAddressField(
        unique=True,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=200, default='Started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # GETTERS
    @property
    def hostname(self):
        """
            Returns the hostname of this VM.
            This is a getter.
        """

        return f"{self.base_vm_name}-{self.vm_name}"

    # SETTERS

    # OPERATORS

    def __str__(self):
        """Returns the hostname of this VM."""
        return self.hostname

    # CONSTRAINTS

    class Meta:
        """
            Here we define the unique constraints.
        """

        constraints = [
            models.UniqueConstraint(
                fields=['vm_name', 'base_vm_name'],
                name='unique_hostname_constraint',
            ),
        ]


class PostgreSQLInstance(models.Model):
    """Represents PostgreSQL cluster."""

    # ATTRIBUTES

    port = models.IntegerField(default=5432)
    version = models.CharField(max_length=10)

    # Foreign Keys

    vm = models.ForeignKey('PostgreSQLVM', on_delete=models.CASCADE)

    # SETTERS

    # OPERATORS

    def __str__(self):
        return f"VM: {self.vm}; Port: {self.port}"

    # CONSTRAINTS

    class Meta:
        """
            Here we define the unique constraints.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['vm', 'port'],
                name='unique_port_per_vm',
            )
        ]


class PostgreSQLDatabase(models.Model):

    """Represents the PostgreSQL database."""

    # ATTRIBUTES

    db_name = models.CharField(max_length=200)
    encoding = models.CharField(max_length=200)
    collate = models.CharField(max_length=200)
    ctype = models.CharField(max_length=200)
    access_privileges = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )
    size = models.CharField(max_length=200)  # this needs adjustment
    tablespace = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    # Foreign Keys

    instance = models.ForeignKey(
        'PostgreSQLInstance',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey('PostgreSQLUser', on_delete=models.CASCADE)

    # GETTERS

    # SETTERS

    # OPERATORS

    def __str__(self):
        return (
            f"PostgreSQL Instance: {self.instance}; "
            f"DB_name: {self.db_name}; "
            f"Owner: {self.owner}"
        )

    class Meta:
        """
            Here we define the unique constraints.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['db_name', 'instance'],
                name='unique_name_instance_owner',
            )
        ]


class BackupSchedule(models.Model):
    """Represents the Backup schedule."""

    class ScheduleType(models.TextChoices):
        """Represents the ScheduleType enum."""
        IMMEDIATE = 'IMMEDIATE'
        ONCE = 'ONCE'
        INTERVAL = 'INTERVAL'
        CRON = 'CRON'

    class Period(models.TextChoices):
        SECOND = 'SECOND'
        MINUTE = 'MINUTE'
        HOUR = 'HOUR'
        DAY = 'DAY'
        WEEK = 'WEEK'
        MONTH = 'MONTH'

    schedule_type = models.CharField(
        max_length=20,
        choices=ScheduleType.choices,
        default=ScheduleType.IMMEDIATE,
    )

    # for schedule_type = "ONCE"

    execute_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # for schedule_type = "INTERVAL"

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

    @classmethod
    def create_immediate(cls):
        """Represents the immediate schedule."""

        return cls(
            schedule_type=cls.ScheduleType.IMMEDIATE,
        )

    @classmethod
    def create_once(cls, execute_at: datetime):
        """Represents the once schedule."""

        return cls(
            schedule_type = cls.ScheduleType.ONCE,
            execute_at = execute_at
        )

    @classmethod
    def create_interval(cls, every: int, period: Period):
        """Represents the interval schedule."""

        return cls(
            schedule_type = cls.ScheduleType.INTERVAL,
            every = every,
            period = period
        )


    @classmethod
    def create_cron(cls, cron: str):
        """Represents the cron schedule."""
        return cls(
            schedule_type = cls.ScheduleType.CRON,
            cron = cron
        )

    def validate(self):
        if self.schedule_type == BackupSchedule.ScheduleType.IMMEDIATE:
            if self.execute_at is not None:
                raise ValidationError("execute_at is only allowed for ONCE schedules.")
            if self.every is not None:
                raise ValidationError("every is only allowed for INTERVAL schedules.")
            if self.period is not None:
                raise ValidationError("period is only allowed for INTERVAL schedules.")
            if self.cron is not None:
                raise ValidationError("cron is only allowed for CRON schedules.")

        elif self.schedule_type == BackupSchedule.ScheduleType.ONCE:
            if self.execute_at is None:
                raise ValidationError("execute_at is required for ONCE schedules.")
            if self.every is not None:
                raise ValidationError("every is only allowed for INTERVAL schedules.")
            if self.period is not None:
                raise ValidationError("period is only allowed for INTERVAL schedules.")
            if self.cron is not None:
                raise ValidationError("cron is only allowed for CRON schedules.")
            if self.execute_at < timezone.now():
                raise ValidationError("the time you mentioned is from the past.")

        elif self.schedule_type == BackupSchedule.ScheduleType.INTERVAL:
            if self.execute_at is not None:
                raise ValidationError("execute_at is only allowed for ONCE schedules.")
            if self.every is None:
                raise ValidationError("every is required for INTERVAL schedules.")
            if self.period is None:
                raise ValidationError("period is required for INTERVAL schedules.")
            if self.cron is not None:
                raise ValidationError("cron is only allowed for CRON schedules.")
            if self.every <= 0:
                raise ValidationError("there cannot be negative or zero intervals.")

        elif self.schedule_type == BackupSchedule.ScheduleType.CRON:
            if self.execute_at is not None:
                raise ValidationError("execute_at is only allowed for ONCE schedules.")
            if self.every is not None:
                raise ValidationError("every is only allowed for INTERVAL schedules.")
            if self.period is not None:
                raise ValidationError("period is only allowed for INTERVAL schedules.")
            if self.cron is None:
                raise ValidationError("cron is required for CRON schdeules.")
        else:
            raise ValidationError("Unknown schedule type.")

class PostgreSQLBackup(models.Model):

    """Represents the PostgreSQL backup."""

    # ATTRIBUTES

    backup_type = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    schedule = models.OneToOneField(
        BackupSchedule,
        on_delete=models.CASCADE,
    )
    backup_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    stanza = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    start_at = models.DateTimeField(
        auto_now_add=True
    )
    stop_at = models.DateTimeField(
        auto_now_add=True
    )
    wal_start = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    wal_stop = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    cluster_size = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )  # needs adjustment
    cluster_backup_size = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )  # needs adjustment
    backup_size = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )  # needs adjustment
    backup_set_size = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )  # needs adjustment

    # Foreign Keys

    instance = models.ForeignKey(
        'PostgreSQLInstance',
        on_delete=models.CASCADE
    )

    # GETTERS

    # SETTERS

    # OPERATORS

    def __str__(self):
        return f"PostgreSQL Instance: {self.instance}"



class PostgreSQLUser(models.Model):
    """
        Represents the PostgreSQL user.
    """

    # ATTRIBUTES

    name = models.CharField(max_length=200, unique=True)

    # OPERATORS

    def __str__(self):
        return f"User: {self.name}"
