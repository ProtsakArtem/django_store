# Generated by Django 5.0.6 on 2024-07-20 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(default='None', max_length=255),
        ),
    ]