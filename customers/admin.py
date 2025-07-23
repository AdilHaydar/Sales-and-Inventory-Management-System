from django.contrib import admin
from .models import Customer
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_email', 'contact_phone')
    search_fields = ('company_name', 'contact_email')
    list_filter = ('company_name',)
    ordering = ('company_name',)

admin.site.register(Customer, CustomerAdmin)