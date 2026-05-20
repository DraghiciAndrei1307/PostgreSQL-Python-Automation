from django.db import models

# Create your models here.

class PostgreSQLVM(models.Model):

    name = models.CharField(max_length=200, unique=True)
    hostname = models.CharField(max_length=200, unique=True)
    ip_address = models.GenericIPAddressField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=200, default='Started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name





