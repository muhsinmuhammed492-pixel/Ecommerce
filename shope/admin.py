from django.contrib import admin
from .models import Product,CartItem,Order,Category
# Register your models here.
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Category)
