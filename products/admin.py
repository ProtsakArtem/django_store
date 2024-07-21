from django.contrib import admin
from products.models import Product, ProductCategory, Cart

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category_name')
    fields = ('name', 'price', 'description', 'quantity', 'image', 'category_name')
    search_fields = ('name', 'category_name__name', 'description')
    ordering = ('name',)


class CartAdmin(admin.TabularInline):
    model = Cart
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0