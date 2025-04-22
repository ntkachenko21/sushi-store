from django.contrib import admin

from checkout.models import Cart, CartItem
from product.models import Category, Product, Ingredient


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(Cart)
admin.site.register(CartItem)