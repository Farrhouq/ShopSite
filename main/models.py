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
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shops')
    date_created = models.DateField(auto_now_add=True)
    # logo = models.ImageField(upload_to='store_logos/', null=True, blank=True)
    # pickup_stations = models.

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.owner}: {self.name}"


class Product(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True)
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_6 = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField('Quantity required')
    cart = models.ForeignKey('Cart', on_delete=models.SET_NULL, null=True, related_name='products')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    # products = models.ManyToManyField(ProductOrder, related_name='products')

    def calc_price(self):
        total = 0
        for product in self.products.all():
            if product.product.price is not None:
                total += float(product.product.price)
        return total


class PickupStation(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    products_ordered = models.ManyToManyField(ProductOrder)
    PICKUP_STATIONS_CHOICES = ((pickup_station, pickup_station.name)
                               for pickup_station in PickupStation.objects.all())
    pickup_station = models.ForeignKey(PickupStation,
                                       choices=PICKUP_STATIONS_CHOICES,
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True)
    # pickup_station = models.TextField()
