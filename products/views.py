from django.shortcuts import render
from products.models import Product, ProductCategory
# Create your views here.

def index(request):
    return render(request, 'products/index.html')

def products(request):
    content = {"title": "Store - Каталог", "products": Product.objects.all(), 'categories': ProductCategory.objects.all()}
    return render(request, 'products/products.html', content)