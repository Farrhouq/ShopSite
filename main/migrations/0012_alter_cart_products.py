# Generated by Django 4.1.3 on 2022-12-21 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_product_description_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='products', to='main.product'),
        ),
    ]
