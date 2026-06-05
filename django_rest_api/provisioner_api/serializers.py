"""
    This module contains the serializers definitions.
"""
from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import PostgreSQLVM, PostgreSQLDatabase, \
    PostgreSQLBackup, PostgreSQLInstance, PostgreSQLUser


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

class PostgreSQLBackupSerializer(serializers.HyperlinkedModelSerializer):
    """
        This is the serializer for the PostgreSQLBackup model.
    """

    class Meta:
        """
            Here we set the model and the DB fields
            we want to expose.
        """

        model = PostgreSQLBackup
        fields = '__all__'

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
