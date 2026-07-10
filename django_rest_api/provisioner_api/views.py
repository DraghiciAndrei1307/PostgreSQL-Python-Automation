"""
    This module contains all the ViewSets definitions.
"""

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .models import PostgreSQLVM, PostgreSQLDatabase, \
    PostgreSQLInstance, PostgreSQLBackup, PostgreSQLUser
from .serializers import GroupSerializer, UserSerializer, \
    PostgreSQLVMSerializer, PostgreSQLInstanceSerializer, \
    PostgreSQLDatabaseSerializer, PostgreSQLBackupSerializer, \
    PostgreSQLUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostgreSQLVMViewSet(viewsets.ModelViewSet):
    """
        This is the ViewSet for the PostgreSQLVM model.
    """

    queryset = PostgreSQLVM.objects.all().order_by("-created_at")
    serializer_class = PostgreSQLVMSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
            We override the perform_create method so that we
            trigger the provisioning when a request is made.
        """
        instance = serializer.save(status="Queued")

        # send the task to the Celery and Redis

        from .tasks import run_ansible_provisioning_task
        run_ansible_provisioning_task.delay(instance.id)

    def partial_update(self, request, *args, **kwargs):
        """
            We override the partial_update method so that we
            can update the IPv4 address of the VM when performing
            a PATCH request.

            The partial_update method is similar to the 'update'
             method, except that all fields for the update will
             be optional. This suits best for a PATCH request
             when we need to update certain fields.
        """

        response = super().partial_update(request, *args, **kwargs)

        ip_sent = request.data.get('ipv4_address')

        if ip_sent:
            pk = kwargs.get('pk')
            PostgreSQLVM.objects.filter(pk=pk).update(ipv4_address=ip_sent)

            print(f"\nThe IP {ip_sent} was saved for the VM with ID {pk}\n")

        return response


class PostgreSQLInstanceViewSet(viewsets.ModelViewSet):
    """
        This is the ViewSet for the PostgreSQLInstance model.
    """

    queryset = PostgreSQLInstance.objects.all().order_by("-port")
    serializer_class = PostgreSQLInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostgreSQLDatabaseViewSet(viewsets.ModelViewSet):
    """
        This is the ViewSet for the PostgreSQLDatabase model.
    """

    queryset = PostgreSQLDatabase.objects.all().order_by("-db_name")
    serializer_class = PostgreSQLDatabaseSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostgreSQLBackupViewSet(viewsets.ModelViewSet):
    """
        This is the ViewSet for the PostgreSQLBackup model.
    """

    queryset = PostgreSQLBackup.objects.all().order_by("-stanza")
    serializer_class = PostgreSQLBackupSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
            We override the perform_create method so that we
            trigger the backup procedure when a request is made.
        """

        instance = serializer.save(status="Queued")

        # we need to import a task here

        from .tasks import perform_backup
        perform_backup.delay(instance.id)

    def partial_update(self, request, *args, **kwargs):
        """
            We override the partial_update method so that we
            can update the instance with the all necessary data
            of the recently created backup.
        """

        response = super().partial_update(request, *args, **kwargs)

        # We extract the data we received from the request

        # stanza = request.data.get('satanza')
        # ...


class PostgreSQLUserViewSet(viewsets.ModelViewSet):
    """
        This is the ViewSet for the PostgreSQLUser model.
    """

    queryset = PostgreSQLUser.objects.all().order_by("-name")
    serializer_class = PostgreSQLUserSerializer
    permissions_classes = [permissions.IsAuthenticated]
