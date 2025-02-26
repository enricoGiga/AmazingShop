from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['supplier', 'name', 'product_code', 'price', 'main_image', 'stock_status']
