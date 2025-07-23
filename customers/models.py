from django.db import models

# Create your models here.

class Customer(models.Model):
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['company_name']