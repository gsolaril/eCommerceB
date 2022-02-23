from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

price = [ MinValueValidator(Decimal("0.01")) ]
zero = [ MinValueValidator(Decimal("0.0")) ]

class Account(models.Model):

    ID = models.CharField(max_length = 255, primary_key = True)
    name = models.CharField(max_length = 255)
    surname = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 255)
    token = models.CharField(max_length = 255)
    avatar = models.CharField(max_length = 255)
    birth = models.DateField(null = True)

class Address(models.Model):

    account = models.ForeignKey(to = Account, on_delete = models.CASCADE)
    pin = models.PositiveIntegerField()
    address = models.CharField(max_length = 255, null = False)
    address2 = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 11, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)

class Shop(models.Model):

    name = models.CharField(max_length = 255)
    description = models.TextField()
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 255)
    opensAt = models.TimeField(default = "00:00")
    closesAt = models.TimeField(default = "00:00")
    unavailable = models.BooleanField(default = False)
    pin = models.PositiveIntegerField()
    address = models.CharField(max_length = 255, null = False)
    address2 = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 11, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 8)
    deliveryCost = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    deliveryRange = models.PositiveIntegerField(default = 0, validators = zero)
    image = models.CharField(max_length = 255)

class Product(models.Model):

    name = models.CharField(max_length = 255, primary_key = True)
    slug = models.SlugField(null = True)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, validators = zero, null = True)
    last_update = models.DateTimeField(auto_now = True)
    description = models.TextField()
    images = models.TextField()

class Model(models.Model):

    product = models.ForeignKey(to = Product, on_delete = models.CASCADE)
    qmin = models.PositiveIntegerField()
    qmax = models.PositiveIntegerField()
    qstep = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2, validators = price)
    discount = models.PositiveIntegerField()

class Delivery(Account):

    since = models.DateField(auto_now = True)
    requests = models.PositiveIntegerField()
    miles = models.DecimalField(max_digits = 4, decimal_places = 1, validators = zero)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, validators = zero)
    shops = models.JSONField()

class Review(models.Model):

    account = models.ForeignKey(to = Account, on_delete = models.SET_NULL, null = True)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    content_object = GenericForeignKey()
    object_id = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    when = models.DateTimeField(auto_now = True)
    review = models.TextField()

#class ProductReview(Review): product = models.ForeignKey(to = Product, on_delete = models.CASCADE)
#class ShopReview(Review): shop = models.ForeignKey(to = Shop, on_delete = models.CASCADE)
#class DeliReview(Review): delivery = models.ForeignKey(to = Delivery, on_delete = models.CASCADE)

class Order(models.Model):

    STATUS = { "pg": "pending", "pd": "paid", "st": "sent", "ok": "done", "er": "error" }

    when = models.DateTimeField(auto_now = True)
    status = models.CharField(choices = STATUS.items(), default = "pg", max_length = 8)
    shop = models.ForeignKey(to = Shop, on_delete = models.SET_NULL, null = True)
    address = models.ForeignKey(to = Address, on_delete = models.SET_NULL, null = True)
    delivery = models.OneToOneField(to = Delivery, on_delete = models.SET_NULL, null = True)
    gross = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    coupons = models.JSONField()
    tax = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    discount = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    deliCost = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    amount = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    reviews = models.JSONField()
    cart = models.JSONField()

class Payment(models.Model):

    PAYMENT_MODES = { "pe": "personal", "mp": "mercpago" }

    order = models.OneToOneField(to = Order, on_delete = models.CASCADE, primary_key = True)
    transaction = models.PositiveIntegerField()
    paymentMode = models.CharField(choices = PAYMENT_MODES.items(), default = "pe", max_length = 8)
    amount = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    when = models.DateTimeField(auto_now = True)

class Coupon(models.Model):

    expires = models.DateField(null = True)
    discount = models.JSONField()
