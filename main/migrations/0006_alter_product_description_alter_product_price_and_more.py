# Generated by Django 4.1.4 on 2022-12-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_product_image_alter_product_store"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="stock",
            field=models.IntegerField(blank=True),
        ),
    ]
