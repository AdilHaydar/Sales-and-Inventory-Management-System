from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from .serializers import ProductSerializer
from ..models import Product
from rest_framework.decorators import action

class ProductViewSet(ListModelMixin ,GenericViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    
    @action(detail=True, methods=['get'])
    def get_product_price(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        return Response({"price": product.price})
    
