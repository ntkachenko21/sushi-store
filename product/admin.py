from django.contrib import admin

from product.models import Category, Product, Ingredient


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Ingredient)
