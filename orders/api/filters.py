import django_filters
from django.db.models import Q
from ..models import Order

class OrderFilter(django_filters.FilterSet):
    order_date_gte = django_filters.DateFilter(field_name="order_date", lookup_expr='gte')
    order_date_lte = django_filters.DateFilter(field_name="order_date", lookup_expr='lte')

    customer = django_filters.NumberFilter(field_name="customer__id")
    product = django_filters.NumberFilter(field_name="product__id")

    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Order
        fields = ['order_date_gte', 'order_date_lte', 'customer', 'product', 'status', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(customer__company_name__icontains=value) |
            Q(product__name__icontains=value)
        )
