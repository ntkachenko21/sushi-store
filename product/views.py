from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from product.models import Product, Category, Ingredient


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "product/index.html", context=context)


class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["allergens"] = product.ingredients.filter(is_allergen=True)
        return context