# Generated by Django 4.1.4 on 2023-02-02 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0035_order_date_placed_order_date_to_be_delivered"),
    ]

    operations = [
        migrations.RenameField(
            model_name="store",
            old_name="logo",
            new_name="picture",
        ),
    ]
