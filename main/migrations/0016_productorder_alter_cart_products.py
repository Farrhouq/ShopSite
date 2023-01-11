# Generated by Django 4.1.4 on 2023-01-11 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_pickupstation_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(verbose_name="Quantity required")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="main.product",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="cart",
            name="products",
            field=models.ManyToManyField(
                related_name="products", to="main.productorder"
            ),
        ),
    ]