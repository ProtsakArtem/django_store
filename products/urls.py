from django.urls import path

from products.views import add_product_to_cart, remove_product_from_cart, IndexView, ProductView

app_name = 'products'



urlpatterns = [
    path('/', ProductView.as_view(), name='index'),
    path('/page/<int:page>/', ProductView.as_view(), name='paginator'),
    path('/category/<int:category_id>/', ProductView.as_view(), name='category'),
    path("/carts/add/<int:product_id>/", add_product_to_cart, name="add_product_to_cart"),
    path('/carts/remove/<int:cart_id>/', remove_product_from_cart, name="remove_product_from_cart")
]