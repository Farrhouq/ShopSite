# Generated by Django 4.1.3 on 2023-01-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_cart_products_remove_order_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
