# Generated by Django 4.1.4 on 2023-01-11 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_productorder_alter_cart_products"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pickupstation",
            name="store",
        ),
    ]
