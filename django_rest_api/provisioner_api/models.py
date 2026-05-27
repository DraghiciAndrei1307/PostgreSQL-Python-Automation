from django.db import models

# Create your models here.

class PostgreSQLVM(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    hostname = models.CharField(max_length=200, unique=True)
    ip_address = models.GenericIPAddressField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=200, default='Started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PostgreSQLDatabase(models.Model):

    id = models.AutoField(primary_key=True)
    vm_id = models.IntegerField()
    name = models.CharField(max_length=200, unique=True)
    owner = models.CharField(max_length=200, unique=True)
    encoding = models.CharField(max_length=200)
    collate = models.CharField(max_length=200)
    ctype = models.CharField(max_length=200)
    access_privileges = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    tablespace = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class PostgreSQLBackup(models.Model):

    id = models.AutoField(primary_key=True)
    database_id = models.IntegerField()
    type = models.CharField(max_length=200)
    stanza = models.CharField(max_length=200)
    backup_id = models.CharField(max_length=200)
    start_at = models.DateTimeField()
    stop_at = models.DateTimeField()
    wal_start = models.CharField(max_length=200)
    wal_stop = models.CharField(max_length=200)
    cluster_size = models.CharField(max_length=200)
    cluster_backup_size = models.CharField(max_length=200)
    backup_size = models.CharField(max_length=200)
    backup_set_size = models.CharField(max_length=200)
