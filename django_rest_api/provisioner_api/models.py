from django.db import models

# Create your models here.

class PostgreSQLVM(models.Model):

    """ Represents a VM provisioned with PostgreSQL."""

    # ATTRIBUTES

    vm_name = models.CharField(max_length=200)
    base_vm_name = models.CharField(max_length=200)
    ipv4_address = models.GenericIPAddressField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=200, default='Started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # GETTERS
    @property
    def hostname(self):
        return f"{self.base_vm_name}-{self.vm_name}"

    # SETTERS

    # OPERATORS

    def __str__(self):
        """Returns the hostname of this VM."""
        return self.hostname

    # CONSTRAINTS

    class Meta:
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
        return f"VM: {self.vm}; Instance ID: {self.id}; Port: {self.port}"

    # CONSTRAINTS

    class Meta:
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
    access_privileges = models.CharField(max_length=200)
    size = models.CharField(max_length=200) # this needs adjustment
    tablespace = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    # Foreign Keys

    instance = models.ForeignKey('PostgreSQLInstance', on_delete=models.CASCADE)
    owner = models.ForeignKey('PostgreSQLUser', on_delete=models.CASCADE)

    # GETTERS

    # SETTERS

    # OPERATORS

    def __str__(self):
        return f"PostgreSQL Instance: {self.instance}; DB_name: {self.db_name}; Owner: {self.owner}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['db_name', 'instance'],
                name='unique_name_instance_owner',
            )
        ]

class PostgreSQLBackup(models.Model):

    """Represents the PostgreSQL backup."""

    # ATTRIBUTES


    type = models.CharField(max_length=200)
    stanza = models.CharField(max_length=200)
    start_at = models.DateTimeField()
    stop_at = models.DateTimeField()
    wal_start = models.CharField(max_length=200)
    wal_stop = models.CharField(max_length=200)
    cluster_size = models.CharField(max_length=200) # needs adjustment
    cluster_backup_size = models.CharField(max_length=200) # needs adjustment
    backup_size = models.CharField(max_length=200) # needs adjustment
    backup_set_size = models.CharField(max_length=200) # needs adjustment

    # Foreign Keys

    instance = models.ForeignKey('PostgreSQLInstance', on_delete=models.CASCADE)

    # GETTERS

    # SETTERS

    # OPERATORS

    def __str__(self):
        return f"PostgreSQL Instance: {self.instance} Backup ID: {self.id}"

class PostgreSQLUser(models.Model):
    """Represents the PostgreSQL user."""

    # ATTRIBUTES

    name = models.CharField(max_length=200, unique=True)

    # OPERATORS

    def __str__(self):
        return f"User: {self.name}"
