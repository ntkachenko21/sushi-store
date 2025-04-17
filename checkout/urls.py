from django.urls import path
from .views import CartSidebarView

urlpatterns = [
    path('cart/', CartSidebarView.as_view(), name='cart-sidebar'),
]
