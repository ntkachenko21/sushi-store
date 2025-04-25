from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path(
        "products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"
    ),
]

app_name = "product"
