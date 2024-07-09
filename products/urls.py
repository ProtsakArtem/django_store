from django.urls import path

from products.views import products, index


app_name = 'products'



urlpatterns = [
    path('/', products, name='index'),
]