# Generated by Django 4.1.4 on 2023-01-18 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0028_remove_store_image_alter_store_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="product",
            name="product_details",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
