from django.urls import path

from product.views import index, ProductDetailView

urlpatterns = [
    path("", index, name="index"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail")
]

app_name = "product"
