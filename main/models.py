from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    


class Store(models.Model):
    name = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    date_created = models.DateField(auto_now_add=True)


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField()
