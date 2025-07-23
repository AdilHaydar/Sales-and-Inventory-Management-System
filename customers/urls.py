from django.urls import path
from .views import CustomerCreateView, CustomerListView, CustomerUpdateView, CustomerDeleteView

app_name = 'customers'

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('create/', CustomerCreateView.as_view(), name='create'),
    path('update/<int:pk>/', CustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CustomerDeleteView.as_view(), name='delete'),
]
