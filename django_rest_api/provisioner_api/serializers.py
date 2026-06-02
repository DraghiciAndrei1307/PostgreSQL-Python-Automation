from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import PostgreSQLVM, PostgreSQLDatabase, PostgreSQLBackup, PostgreSQLInstance, PostgreSQLUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class PostgreSQLVMSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostgreSQLVM
        fields = '__all__'
        read_only_fields = ['status']

class PostgreSQLInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostgreSQLInstance
        fields = '__all__'

class PostgreSQLDatabaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostgreSQLDatabase
        fields = '__all__'

class PostgreSQLBackupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostgreSQLBackup
        fields = '__all__'

class PostgreSQLUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostgreSQLUser
        fields = '__all__'
