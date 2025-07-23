from django.urls import path
from .views import OrderListView, OrderUpdateView, OrderDeleteView, OrderCreateView, OrderPdfView

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('pdf/', OrderPdfView.as_view(), name='order_pdf'),
]
