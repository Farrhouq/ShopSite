# Generated by Django 4.1.4 on 2023-01-18 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0029_order_completed_product_product_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="store",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="store_logos/"),
        ),
    ]
