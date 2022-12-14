# Generated by Django 4.1.4 on 2022-12-14 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_cart"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="store",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="main.store"
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]