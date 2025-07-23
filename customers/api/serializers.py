from ..models import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'company_name', 'contact_phone', 'contact_email', 'is_active']