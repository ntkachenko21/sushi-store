from django.contrib import admin

from checkout.models import Cart, CartItem


admin.site.register(Cart)
admin.site.register(CartItem)
