# Generated by Django 4.1.4 on 2023-02-07 21:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0041_alter_order_options_alter_notification_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="date",
            field=models.DateTimeField(null=True),
        ),
    ]