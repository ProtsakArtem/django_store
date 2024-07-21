from django.db import models
from products.models import Cart
from users.models import User


# Create your models here.
class Order(models.Model):
    CREATED = 0
    PAID = 1
    DELIVERED = 2
    ON_WAY = 3
    STATUSES = (
        (CREATED, "Создан"),
        (PAID, "Оплачен"),
        (ON_WAY, "В пути"),
        (DELIVERED, "Доставлен"),
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=32, default=0)
    address = models.CharField(max_length=255, default="None")
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"


    def update_after_payment(self):
        carts = Cart.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchaced_items': [cart.de_json() for cart in carts],
            'total_sum': float(carts.total_sum())
        }
        carts.delete()
        self.save()
