from rest_framework import serializers
from ..models import Order

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ['id', 'customer', 'product', 'quantity', 'price', 'order_date', 'status', 'total_price']
        read_only_fields = ['id', 'order_date', 'total_price']

    def validate(self, attrs):
        if attrs['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if attrs['price'] < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return attrs