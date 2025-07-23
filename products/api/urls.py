from .views import ProductViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'products_api'

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
