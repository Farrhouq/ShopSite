from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    


class Store(models.Model):
    name = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.owner}: {self.name}"


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.FloatField(blank=True)
    image = models.ImageField(upload_to='images/', null=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(blank=True)
