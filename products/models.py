from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_instance = type(self).objects.get(pk=self.pk)
            if self.stock < 0:
                raise ValueError("Değişiklik Sonrası Ürün Stoğu Negatif Olamaz! Mevcut Stok: {}".format(old_instance.stock))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']