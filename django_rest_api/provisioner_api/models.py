"""
    In this module we define our models.
"""

from django.db import models


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


class PostgreSQLBackup(models.Model):

    """Represents the PostgreSQL backup."""

    # ATTRIBUTES

    backup_type = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    backup_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    execute_at = models.DateTimeField(
        null=True,
        blank=True
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
