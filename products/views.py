from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView

from common.views import TitleMixin
from products.models import Product, ProductCategory, Cart


# Create your views here.

class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = "Store"


class ProductView(TitleMixin, ListView):
    model = Product
    paginate_by = 3
    template_name = 'products/products.html'
    title = "Store - Каталог"

    def get_queryset(self):
        queryset = super(ProductView, self).get_queryset().order_by('id')
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_name=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoies = cache.get('categoies')
        if not categoies:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categoies', context['categories'], 30)
        else:
            context['categories'] = categoies
        return context

@login_required
def add_product_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    carts = Cart.objects.filter(user=request.user, product=product)
    if carts.exists():
        cart = carts.first()
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(user=request.user, product=product, quantity=1)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_product_from_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))