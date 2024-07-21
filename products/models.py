from django.db import models

from users.models import User


# Create your models here.




class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(max_length=255, upload_to="product_images")
    category_name = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.category_name.name}"


class CartQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(cart.sum() for cart in self)

    def total_quantity(self):
        return sum(cart.quantity for cart in self)


class Cart(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f"Корзина: {self.user.username} | Продукт: {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price

    def de_json(self):
        cart_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return cart_item

