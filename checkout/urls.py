from django.urls import path
from checkout.views import (
    CartSidebarView,
    AddToCartView,
    CheckoutPageView,
)

urlpatterns = [
    path("cart/", CartSidebarView.as_view(), name="cart-sidebar"),
    path("checkout/", CheckoutPageView.as_view(), name="checkout-page"),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
]

app_name = "checkout"
