from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.template.defaultfilters import slugify
import datetime


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_pending_deliveries_count(self):
        return len([order for order in self.orders_placed.all() if order.get_status() == 'Approved, Pending Delivery' ])

    def get_pending_deliveries(self):
        return self.orders_placed.filter(~Q(delivery_date=None))

    def get_new_notifications(self):
        return self.notifications.filter(is_read=False)

    def get_all_notifications(self):
        return self.notifications.all()

    def __str__(self):
        return self.username

 
class Store(models.Model):
    name = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shops')
    date_created = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to='store_logos/', null=True, blank=True, default='/store_logos/shop.jpg')
    category = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['-date_created']

    def get_unprocessed_orders(self):
        return self.orders.filter(delivery_date=None)

    def get_completed_orders(self):
        return [order for order in self.orders.all() if order.is_completed()]

    def get_completed_orders_count(self):
        return len([order for order in self.orders.all() if order.is_completed()])

    def __str__(self):
        return f"{self.owner}: {self.name}"

    def get_slug(self):
        return slugify(self.name)


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
    product_details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductOrder(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField('Quantity required')
    cart = models.ForeignKey(
        'Cart', on_delete=models.SET_NULL, null=True, related_name='products')


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    # products = models.ManyToManyField(ProductOrder, related_name='products')

    def calc_price(self):
        total = 0
        for product in self.products.all():
            if product.product.price is not None:
                total += float(product.product.price)*product.quantity
        return total


class PickupStation(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='orders_placed')
    user_name = models.CharField(max_length=200, null=True, blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='orders')
    products_ordered = models.ManyToManyField(ProductOrder, related_name='products_ordered')
    location_details = models.JSONField(null=True, blank=True)
    date_placed = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    

    class Meta:
        ordering = ['-date_placed']

    def is_completed(self):
        if self.delivery_date and self.delivery_date < datetime.date.today():
            return True
        return False

    def get_status(self):
        if self.delivery_date is None:
            return 'Pending Approval'
        elif self.delivery_date is not None and not self.is_completed():
            return 'Approved, Pending Delivery'
        elif self.is_completed():
            return 'Completed'

    def calc_price(self):
        total = 0
        for product in self.products_ordered.all():
            if product.product.price is not None:
                total += float(product.product.price)*product.quantity
        return total

class Notification(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)
    TYPE_CHOICES = (
        ('ORDER UPDATE', 'o'),
        ('NEW ORDER', 'n')
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=12, null=True)
    details = models.JSONField(null=True)

    def get_url(self):
        next = f'?from={self.id}'
        if self.type == 'ORDER UPDATE':
            return f'/{self.to}/orders/{self.details["order_pk"]}'+next
        elif self.type == 'NEW ORDER':
            return f'/{self.to}/{self.details["shop_slug"]}/process-order/{self.details["order_pk"]}'+next

    class Meta:
        ordering = ['-date']