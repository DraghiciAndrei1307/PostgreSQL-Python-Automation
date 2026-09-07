"""
    In this module we define our infrastructure models.
"""
from datetime import datetime
from django.utils import timezone

from django.db import models
from django.core.exceptions import ValidationError

from definitions import BackupClass

class VM(models.Model):

    """Represents the VM model."""

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

class InfrastructureVM(VM):
    """
    Represents the Infrastructure VM model
    used for storing our backups.
    """

class BackupStorage(models.Model):

    backup = models.ForeignKey(
        BackupClass,
        on_delete=models.CASCADE,
        related_name='stored_backups',
    )

    infrastructure_vm = models.ForeignKey(
        InfrastructureVM,
        on_delete=models.CASCADE,
        related_name='storage_locations',
    )

    path = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['backup', 'infrastructure_vm'],
                name='unique_storage_location',
            )
        ]

