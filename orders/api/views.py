from .serializers import OrderSerializer
from rest_framework.generics import ListAPIView
from ..models import Order
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter
from rest_framework.renderers import JSONRenderer

class OrderListView(ListAPIView):
    queryset = Order.objects.filter(customer__is_active=True).order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    renderer_classes = [JSONRenderer]

