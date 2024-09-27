from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Product(models.Model):
    IN_STOCK = 'In stock'
    OUT_OF_STOCK = 'Out of stock'

    STOCK_STATUS_CHOICES = [
        (IN_STOCK, 'In stock'),
        (OUT_OF_STOCK, 'Out of stock')
    ]

    supplier = models.ForeignKey('Supplier',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES,
                                    default=IN_STOCK)

    class Meta:
        unique_together = ('supplier',
                           'product_code')

    def __str__(self):
        return f"{self.name} ({self.product_code})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image_url = models.TextField()
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            ProductImage.objects.filter(product=self.product, is_default=True).update(
                is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name} (Default: {self.is_default})"
