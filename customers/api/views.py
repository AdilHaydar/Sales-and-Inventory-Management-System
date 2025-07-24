from rest_framework.generics import ListAPIView
from .serializers import CustomerSerializer
from ..models import Customer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CustomerFilter

class CustomerListView(ListAPIView):
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilter
    