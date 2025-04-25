from django.views import generic
from django.views.generic import ListView

from product.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = "product/index.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["products"] = Product.objects.prefetch_related("ingredients")

        return context


class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product = Product.objects.prefetch_related("ingredients").get(id=product.id)
        context["allergens"] = product.ingredients.filter(is_allergen=True)
        return context
