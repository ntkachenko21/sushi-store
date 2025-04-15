from django.urls import path

from product.views import index

urlpatterns = [
    path("", index, name="index"),

]

app_name = "product"
