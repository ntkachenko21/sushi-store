from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from product.models import Product, Category, Ingredient


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "product/index.html", context=context)
