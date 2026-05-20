from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .models import PostgreSQLVM
from .serializers import GroupSerializer, UserSerializer, PostgreSQLVMSerializer

from pg_provisioner import PgProvisioner

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

    queryset = PostgreSQLVM.objects.all().order_by("-created_at")
    serializer_class = PostgreSQLVMSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        instance = serializer.save(status="Queued")

        # send the task to the Celery and Redis

        from .tasks import run_ansible_provisioning_task
        run_ansible_provisioning_task.delay(instance.id)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        ip_sent = request.data.get('ip_address')

        if ip_sent:
            instance.ip_address = ip_sent
            instance.save()

            print(f"\nThe IP {ip_trimis} was saved for the VM {instance.name}!\n")

        return super().partial_update(request, *args, **kwargs)


