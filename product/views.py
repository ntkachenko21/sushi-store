from django.views import generic
from django.views.generic import ListView

from checkout.utils import get_user_cart
from product.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = "product/index.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["products"] = Product.objects.prefetch_related("ingredients")
        cart_data = get_user_cart(self.request)
        context["cart"] = {
            "cart_quantity": cart_data.get("total_quantity"),
            "cart_total_price": cart_data.get("total_price")
        }
        print(context["cart"])

        return context


class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product = Product.objects.prefetch_related("ingredients").get(id=product.id)
        context["allergens"] = product.ingredients.filter(is_allergen=True)
        return context
