from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View

from product.models import Product


class CartSidebarView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(pk__in=cart.keys())
        cart_items = [
            {'product': product, 'quantity': cart[str(product.pk)]}
            for product in products
        ]
        html = render_to_string('checkout/cart_sidebar.html', {'cart_items': cart_items}, request=request)
        return JsonResponse({'html': html})
