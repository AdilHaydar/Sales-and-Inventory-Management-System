from .views import OrderListView
from django.urls import path

app_name = 'orders_api'
urlpatterns = [
    path('api/v1/orders/', OrderListView.as_view(), name='order_list'),
    # Add other order-related URLs here
]