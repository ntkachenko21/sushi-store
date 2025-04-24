from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View
import json

from checkout.models import CartItem, Cart
from product.models import Product


class CartSidebarView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_items = cart.items.select_related('product')
            total_price = sum(item.product.price * item.quantity for item in cart_items)
        else:
            cart_items = []
            total_price = 0
            session_cart = request.session.get("cart", {})
            if session_cart:
                product_ids = session_cart.keys()
                products = Product.objects.filter(id__in=product_ids).prefetch_related('category')
                for product in products:
                    cart_items.append({
                        "product": product,
                        "quantity": session_cart[str(product.id)],
                        "total_price": product.price * session_cart[str(product.id)]
                    })
                    total_price += product.price * session_cart[str(product.id)]

        html = render_to_string(
            "checkout/sidebar.html",
            {
                "cart_items": cart_items,
                "total_price": f"{total_price:.2f}"
            },
            request=request
        )
        return JsonResponse({"html": html})


class CheckoutPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_items = cart.items.select_related('product')
            total_price = sum(item.product.price * item.quantity for item in cart_items)
        else:
            cart_items = []
            total_price = 0
            session_cart = request.session.get("cart", {})
            if session_cart:
                product_ids = session_cart.keys()
                products = Product.objects.filter(id__in=product_ids).prefetch_related('category')
                for product in products:
                    cart_items.append({
                        "product": product,
                        "quantity": session_cart[str(product.id)],
                        "total_price": product.price * session_cart[str(product.id)]
                    })
                    total_price += product.price * session_cart[str(product.id)]

        context = {
            "cart_items": cart_items,
            "total_price": total_price,
        }

        return render(request, "checkout/checkout_page.html", context)


class AddToCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = str(data.get("product_id"))
            quantity = int(data.get("quantity", 1))
            print(f"Received data: product_id={product_id}, quantity={quantity}")
        except (ValueError, json.JSONDecodeError):
            print("Error parsing JSON data")
            return JsonResponse(
                {"success": False, "error": "Invalid data"}, status=400
            )

        try:
            product = Product.objects.get(pk=product_id)
            print(f"Found product: {product.title}, price={product.price}")
        except Product.DoesNotExist:
            print(f"Product with ID {product_id} not found")
            return JsonResponse(
                {"success": False, "error": "Product not found"}, status=404
            )

        if request.user.is_authenticated:
            print("User is authenticated.")
            cart = request.user.cart
            if not cart:
                print("No cart found for user, creating a new one.")
                cart = Cart.objects.create(session_key=request.session.session_key)
                request.user.cart = cart
                request.user.save()
            print(f"cart_id: {cart.id}, cart_items: {cart.items.all()}")

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
            if created:
                print(f"CartItem created: {cart_item.product.title}, quantity={cart_item.quantity}")
            else:
                print(f"CartItem found and updated: {cart_item.product.title}, current quantity={cart_item.quantity}")

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity

            cart_item.save()
            print(f"Updated CartItem: {cart_item.product.title}, new quantity={cart_item.quantity}")

            cart_items = cart.items.all()
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            total_quantity = sum(item.quantity for item in cart_items)
            print(f"Total price after update: {total_price}, Total quantity after update: {total_quantity}")

        else:
            print("User is not authenticated, using session.")
            cart = request.session.get("cart", {})
            print(f"Cart from session before update: {cart}")

            if product_id in cart:
                cart[product_id] += quantity
                print(f"Updated product {product_id} quantity in session cart: {cart[product_id]}")
            else:
                cart[product_id] = quantity
                print(f"Added new product {product_id} to session cart: {cart[product_id]}")

            request.session["cart"] = cart
            print(f"Updated session cart: {cart}")

            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            total_price = sum(product.price * cart[str(product.id)] for product in products)
            total_quantity = sum(cart.values())
            print(f"Total price after update: {total_price}, Total quantity after update: {total_quantity}")

        return JsonResponse(
            {
                "success": True,
                "total_quantity": total_quantity,
                "total_price": f"{total_price:.0f} zł",
            }
        )
