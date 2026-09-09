from ..models import (
    Order,
    ProvisionParameters,
    BackupParameters,
    RestoreParameters,
    DeleteParameters
)
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        """Here we decide which type of parameters to use"""
        pass
