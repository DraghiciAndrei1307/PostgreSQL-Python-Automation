"""
    This module contains the serializers definitions.
"""
from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import PostgreSQLVM, PostgreSQLDatabase, \
    PostgreSQLBackup, PostgreSQLInstance, PostgreSQLUser, BackupSchedule


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the User model.
    """

    class Meta:
        """
            Here we set the model and the DB
            fields we expose.
        """

        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the Group model.
    """

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """

        model = Group
        fields = ["url", "name"]


class PostgreSQLVMSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the PostgreSQLVM model.
    """

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """

        model = PostgreSQLVM
        fields = '__all__'
        read_only_fields = ['status']


class PostgreSQLInstanceSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the PostgreSQLInstance model.
    """

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """

        model = PostgreSQLInstance
        fields = '__all__'


class PostgreSQLDatabaseSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the PostgreSQLDatabase model.
    """

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """

        model = PostgreSQLDatabase
        fields = '__all__'


class BackupScheduleSerializer(serializers.ModelSerializer):

    """
        This is the serializer for the BackupSchedule model.
    """

    class Meta:
        model = BackupSchedule
        fields = '__all__'

class PostgreSQLBackupSerializer(serializers.ModelSerializer):
    """
        This is the serializer for the PostgreSQLBackup model.
    """

    schedule = BackupScheduleSerializer()

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """

        model = PostgreSQLBackup
        fields = ('backup_type', 'schedule', 'instance')

    def create(self, validated_data):

        """
            We overite the create() method
            so that we can create a BackupSchedule
            instance before we create the PostgreSQLBackup.
        """

        # extract schedule data

        schedule_data = validated_data.pop('schedule')

        schedule_type = schedule_data['schedule_type']

        # create the BackupSchedule instance

        backup_schedule = None

        if schedule_type == BackupSchedule.ScheduleType.IMMEDIATE:
            backup_schedule = BackupSchedule.create_immediate()
        elif schedule_type == BackupSchedule.ScheduleType.ONCE:
            backup_schedule = BackupSchedule.create_once(
                execute_at=schedule_data['execute_at']
            )
        elif schedule_type == BackupSchedule.ScheduleType.INTERVAL:
            backup_schedule = BackupSchedule.create_interval(
                every=schedule_data['every'],
                period=schedule_data['period']
            )
        elif schedule_type == BackupSchedule.ScheduleType.CRON:
            backup_schedule = BackupSchedule.create_cron(
                cron=schedule_data['cron'],
            )
        elif schedule_type == BackupSchedule.ScheduleType.BENCHMARK:
            backup_schedule = BackupSchedule.create_benchmark(
                execute_at=schedule_data['execute_at'],
            )

        backup_schedule.save()

        # return the PostgreSQLBackup instance

        return PostgreSQLBackup.objects.create(
            schedule=backup_schedule,
            **validated_data
        )

class PostgreSQLUserSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the PostgreSQLUser model.
    """

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """
        model = PostgreSQLUser
        fields = '__all__'
