from django.db import models

from product.models import Product


class Cart(models.Model):
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def total_price_function(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        self.unit_price = self.product.price or 0
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
