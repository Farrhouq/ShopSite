# Generated by Django 4.1.4 on 2023-02-01 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0031_remove_order_pickup_station_order_address"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="address",
            new_name="location_details",
        ),
    ]