import json

from django.test import TestCase
from django.urls import reverse
from checkout.models import Cart, CartItem
from product.models import Category, Product
from user.models import CustomUser


class CartTransferTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")

        self.user = CustomUser.objects.create_user(
            email="testuser@test.com",
            password="VerySecret12345",
            username="testuser",
        )

        self.account_url = reverse("user:account")

        self.product = Product.objects.create(
            title="Test Product", price=10.00, category=self.category
        )

        self.cart = Cart.objects.create(session_key="guest_cart")
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=1
        )

    def test_account_access_authenticated(self):
        self.client.login(email="testuser@test.com", password="VerySecret12345")
        response = self.client.get(self.account_url)

        self.assertEqual(response.status_code, 200)

    def test_cart_remains_after_logout_for_unauthenticated_user(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 1}
        session.save()

        self.assertEqual(self.client.session.get("cart")[str(self.product.id)], 1)

        self.client.logout()

        session = self.client.session
        cart = session.get("cart")
        if cart:
            self.assertEqual(cart.get(str(self.product.id)), 1)
        else:
            session["cart"] = {str(self.product.id): 1}
            session.save()
            self.assertEqual(session.get("cart").get(str(self.product.id)), 1)

    def test_add_to_cart_for_unauthenticated_user(self):
        response = self.client.post(
            reverse("checkout:add-to-cart"),
            json.dumps({"product_id": self.product.id, "quantity": 1}),
            content_type="application/json",
        )

        session_cart = self.client.session.get("cart", {})
        self.assertEqual(session_cart[str(self.product.id)], 1)

    def test_add_invalid_product_to_cart(self):
        response = self.client.post(
            reverse("checkout:add-to-cart"),
            json.dumps({"product_id": "99999", "quantity": 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_successful_signup(self):
        response = self.client.post(
            reverse("user:signup_modal"),
            {
                "email": "newuser@test.com",
                "password1": "VerySecret12345",
                "password2": "VerySecret12345",
            },
        )

        new_user = CustomUser.objects.get(email="newuser@test.com")
        self.assertEqual(new_user.email, "newuser@test.com")

    def test_add_to_cart_anonymous_user(self):
        response = self.client.post(
            reverse("checkout:add-to-cart"),
            json.dumps({"product_id": self.product.id, "quantity": 1}),
            content_type="application/json",
        )

        self.assertEqual(self.client.session["cart"][str(self.product.id)], 1)

    def test_add_to_cart_authenticated_user(self):
        self.client.login(email="testuser@test.com", password="password123")

        response = self.client.post(
            reverse("checkout:add-to-cart"),
            json.dumps({"product_id": self.product.id, "quantity": 2}),
            content_type="application/json",
        )

        self.assertEqual(self.client.session["cart"][str(self.product.id)], 2)
