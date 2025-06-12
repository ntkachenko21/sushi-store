from django.http import HttpRequest

from product.models import Product


def get_user_cart(request: HttpRequest):
    cart_items, total_price = [], 0

    if request.user.is_authenticated:
        cart = getattr(request.user, "cart", None)
        if not cart:
            cart_items, total_price = [], 0
        else:
            cart_items = cart.items.select_related("product")
            total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        session_cart = request.session.get("cart", {})
        if session_cart:
            product_ids = session_cart.keys()
            products = Product.objects.filter(id__in=product_ids).prefetch_related("category")
            for product in products:
                cart_items.append({
                    "product": product,
                    "quantity": session_cart[str(product.id)],
                    "total_price": product.price * session_cart[str(product.id)]
                })
                total_price += product.price * session_cart[str(product.id)]

    return {"cart_items": cart_items, "total_price": total_price}
