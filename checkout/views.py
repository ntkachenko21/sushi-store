from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from product.models import Product


class CartSidebarView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(pk__in=cart.keys())
        cart_items = []

        total_price = 0

        for product in products:
            quantity = cart[str(product.pk)]
            item_total = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})
            total_price += item_total

        html = render_to_string(
            'checkout/sidebar.html',
            {'cart_items': cart_items, 'total_price': f"{total_price:.2f}"},
            request=request
        )
        return JsonResponse({'html': html})


@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = str(data.get("product_id"))
            quantity = int(data.get("quantity", 1))
        except (ValueError, json.JSONDecodeError):
            return JsonResponse({"success": False, "error": "Invalid data"}, status=400)

        # Проверка на существование товара
        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"}, status=404)

        cart = request.session.get("cart", {})

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session["cart"] = cart

        # calculate total items and total price
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total_price = sum(
            product.price * cart[str(product.id)] for product in products
        )
        total_quantity = sum(cart.values())

        return JsonResponse({
            "success": True,
            "total_quantity": total_quantity,
            "total_price": f"{total_price:.0f} zł"
        })

class CheckoutPageView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(pk__in=cart.keys())

        cart_items = []
        total_price = 0

        for product in products:
            quantity = cart[str(product.pk)]
            item_total = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})
            total_price += item_total

        context = {
            'cart_items': cart_items,
            'total_price': total_price
        }

        return render(request, 'checkout/checkout_page.html', context)
