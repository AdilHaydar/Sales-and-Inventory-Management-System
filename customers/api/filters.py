import django_filters
from ..models import Customer

class CustomerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Customer
        fields = ['search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(company_name__icontains = value)
