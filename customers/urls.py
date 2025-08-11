from django.urls import path
from .views import CustomerCreateView, CustomerListView, CustomerUpdateView, CustomerDeleteView, CustomerDetailView, CustomerCreditListView, CustomerCreditUpdateView, CustomerCreditDetailView

app_name = 'customers'

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('credit/', CustomerCreditListView.as_view(), name='credit_list'),
    path('create/', CustomerCreateView.as_view(), name='create'),
    path('update/<int:pk>/', CustomerUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CustomerDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', CustomerDetailView.as_view(), name='detail'),
    path('credit/detail/', CustomerCreditDetailView.as_view(), name='credit_detail'),
    path('create/credit/', CustomerCreditUpdateView.as_view(), name='create_credit'),
]
