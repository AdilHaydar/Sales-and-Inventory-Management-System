from .views import CustomerListView
from django.urls import path

app_name = 'customers_api'
urlpatterns = [
    path('api/v1/customers/', CustomerListView.as_view(), name='customer_list'),
    # Add other order-related URLs here
]