from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity', 'order_date', 'status')
    search_fields = ('customer__company_name', 'product__name')
    list_filter = ('status', 'order_date')
    ordering = ('-order_date',)

admin.site.register(Order, OrderAdmin)

