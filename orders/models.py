from django.db import models

# Create your models here.

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

class Order(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} for {self.customer.company_name}"
    
    @property
    def total_price(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-order_date']
