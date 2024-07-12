from django.urls import path

from products.views import products, index
from users.views import add_product_to_cart, remove_product_from_cart

app_name = 'products'



urlpatterns = [
    path('/', products, name='index'),
    path("/carts/add/<int:product_id>/", add_product_to_cart, name="add_product_to_cart"),
    path('/carts/remove/<int:cart_id>/', remove_product_from_cart, name="remove_product_from_cart")
]