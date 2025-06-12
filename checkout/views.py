import json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View

from checkout.models import CartItem, Cart
from product.models import Product
from checkout.utils import get_user_cart


class CartSidebarView(View):
    @staticmethod
    def get(request):
        cart = get_user_cart(request)

        html = render_to_string(
            "checkout/sidebar.html",
            {
                "cart_items": cart["cart_items"],
                "total_price": f"{cart["total_price"]:.2f}"
            },
            request=request
        )
        return JsonResponse({"html": html})


class CheckoutPageView(View):
    @staticmethod
    def get(request):
        cart = get_user_cart(request)

        context = {
            "cart_items": cart["cart_items"],
            "total_price": cart["total_price"],
        }

        return render(request, "checkout/checkout_page.html", context)


class AddToCartView(View):
    @staticmethod
    def post(request):
        try:
            data = json.loads(request.body)
            product_id = str(data.get("product_id"))
            quantity = int(data.get("quantity", 1))
        except (ValueError, json.JSONDecodeError):
            return JsonResponse(
                {"success": False, "error": "Invalid data"}, status=400
            )

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Product not found"}, status=404
            )

        if request.user.is_authenticated:
            cart = request.user.cart
            if not cart:
                cart = Cart.objects.create(session_key=request.session.session_key)
                request.user.cart = cart
                request.user.save()

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity

            cart_item.save()

            cart_items = cart.items.all()
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            total_quantity = sum(item.quantity for item in cart_items)

        else:
            cart = request.session.get("cart", {})

            if product_id in cart:
                cart[product_id] += quantity
            else:
                cart[product_id] = quantity

            request.session["cart"] = cart

            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            total_price = sum(product.price * cart[str(product.id)] for product in products)
            total_quantity = sum(cart.values())

        return JsonResponse(
            {
                "success": True,
                "total_quantity": total_quantity,
                "total_price": f"{total_price:.0f} zł",
            }
        )
