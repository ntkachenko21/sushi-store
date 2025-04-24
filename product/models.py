from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=63,
        unique=True,
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=63,
        unique=True
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    weight = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        related_name="products"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(
        max_length=63,
    )
    is_allergen = models.BooleanField()

    def __str__(self):
        return f"{self.name}{" (allergen)" if self.is_allergen else ""}"
