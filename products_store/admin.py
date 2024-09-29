from django.contrib import admin

from products_store.models import Product, Supplier, ProductImage

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(ProductImage)