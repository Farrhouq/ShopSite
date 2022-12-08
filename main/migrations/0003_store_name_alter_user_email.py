# Generated by Django 4.1.4 on 2022-12-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_store_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="store",
            name="name",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
    ]