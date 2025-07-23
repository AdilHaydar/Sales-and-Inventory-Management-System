from rest_framework.generics import ListAPIView
from .serializers import CustomerSerializer
from ..models import Customer

class CustomerListView(ListAPIView):
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    