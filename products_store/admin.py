from django.contrib import admin

from products_store.models import Product, Supplier

admin.site.register(Product)
admin.site.register(Supplier)