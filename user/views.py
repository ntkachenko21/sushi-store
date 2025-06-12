from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import login
from django.views import View
from django_htmx.http import HttpResponseClientRefresh

from product.models import Product
from user.forms import CustomUserCreationForm, CustomLoginForm
from user.models import CustomUser
from checkout.models import Cart, CartItem


class LoginModalView(View):
    def get(self, request):
        form = CustomLoginForm()
        return render(
            request, "includes/modals/login_modal.html", {"form": form}
        )

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseClientRefresh()
        return render(
            request, "includes/modals/login_modal.html", {"form": form}
        )


class SignupModalView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(
            request, "includes/modals/signup_modal.html", {"form": form}
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            session_cart = request.session.get("cart", {})

            if not session_cart:
                pass
            else:
                cart = Cart.objects.create()
                user.cart = cart
                user.save()

                product_ids = session_cart.keys()
                products = Product.objects.filter(id__in=product_ids)

                for product in products:
                    quantity = session_cart.get(str(product.id))
                    if quantity <= 0: continue
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity
                    )

                    cart_item.save()

            return HttpResponseClientRefresh()
        return render(
            request, "includes/modals/signup_modal.html", {"form": form}
        )


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/account.html"
    login_url = "login"

    def get_object(self):
        return self.request.user
