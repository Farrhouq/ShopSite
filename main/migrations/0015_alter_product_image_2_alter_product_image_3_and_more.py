# Generated by Django 4.1.4 on 2022-12-28 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0014_alter_product_image_2_alter_product_image_3_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image_2",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_3",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_4",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
