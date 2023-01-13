# Generated by Django 4.1.4 on 2023-01-13 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0024_remove_pickupstation_store"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="products",
        ),
        migrations.RemoveField(
            model_name="order",
            name="cart",
        ),
        migrations.AddField(
            model_name="order",
            name="products_ordered",
            field=models.ManyToManyField(to="main.productorder"),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="pickup_station",
            field=models.ForeignKey(
                blank=True,
                choices=[],
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.pickupstation",
            ),
        ),
        migrations.AlterField(
            model_name="productorder",
            name="cart",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="main.cart",
            ),
        ),
    ]
