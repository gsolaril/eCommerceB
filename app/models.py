from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User, AbstractBaseUser

# Create your models here.

price = [ MinValueValidator(Decimal("0.01")) ]
zero = [ MinValueValidator(Decimal("0.0")) ]

class User(AbstractBaseUser):

    USERNAME_FIELD = "email"

    user_id = models.PositiveIntegerField(primary_key = True)
    email = models.EmailField(max_length = 64, unique = True)
    name = models.CharField(max_length = 64)
    surname = models.CharField(max_length = 64)
    phone = models.CharField(max_length = 16)
    avatar = models.CharField(max_length = 255, null = True)
    birth = models.DateField(null = True)
    since = models.DateField()
    is_superuser = models.BooleanField(default = False)

class Address(models.Model):

    address_id = models.PositiveIntegerField(primary_key = True)
    user = models.ForeignKey(to = User, on_delete = models.CASCADE)
    latitude = models.DecimalField(max_digits = 11, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 11, decimal_places = 8)
    address = models.CharField(max_length = 255, null = False)
    address2 = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    pin = models.PositiveIntegerField()

class Shop(models.Model):

    shop_id = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 255)
    opens_at = models.TimeField(default = "00:00")
    closes_at = models.TimeField(default = "00:00")
    unavailable = models.BooleanField(default = False)
    pin = models.PositiveIntegerField()
    address = models.CharField(max_length = 255, null = False)
    address2 = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits = 11, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 11, decimal_places = 8)
    delivery_cost = models.DecimalField(max_digits = 6, decimal_places = 2, validators = price)
    delivery_range = models.PositiveIntegerField(default = 0, validators = zero)
    image = models.CharField(max_length = 255)

class Product(models.Model):

    product_id = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 255)
    slug = models.SlugField(null = True)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, validators = zero, null = True)
    last_update = models.DateField(auto_now = True)
    description = models.TextField()
    images = models.TextField()

class Model(models.Model):

    model_id = models.PositiveIntegerField(primary_key = True)
    product = models.ForeignKey(to = Product, on_delete = models.CASCADE)
    model = models.CharField(max_length = 32, null = True)
    qmin = models.PositiveIntegerField()
    qmax = models.PositiveIntegerField()
    price = models.DecimalField(max_digits = 10,
        decimal_places = 2, validators = price)

class Delivery(models.Model): # To be improved as user

    delivery_id = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 64)
    surname = models.CharField(max_length = 64)
    phone = models.CharField(max_length = 16)
    tasks = models.PositiveIntegerField()
    miles = models.DecimalField(max_digits = 4, decimal_places = 1, validators = zero)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, validators = zero)
    since = models.DateField()
    shops = models.JSONField()

class Order(models.Model):

    STATUS = ["pending", "paid", "sent", "done", "error"]
    STATUS_DEF = STATUS[0]
    STATUS = list(zip(STATUS, STATUS))

    order_id = models.PositiveIntegerField(primary_key = True)
    when = models.DateTimeField(auto_now = True)
    status = models.CharField(choices = STATUS, default = STATUS_DEF, max_length = 8)
    user = models.ForeignKey(to = User, on_delete = models.SET_NULL, null = True)
    gross = models.DecimalField(max_digits = 10, decimal_places = 2, validators = price, default = 0)
    coupons = models.JSONField()
    tax = models.DecimalField(max_digits = 10, decimal_places = 2, validators = price, default = 0)
    discount = models.DecimalField(max_digits = 10, decimal_places = 2, validators = price, default = 0)
    deli_cost = models.DecimalField(max_digits = 10, decimal_places = 2, validators = price, default = 0)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, validators = price, default = 0)
    reviewed = models.BooleanField(default = False)
    cart = models.JSONField()
    shop = models.ForeignKey(to = Shop, on_delete = models.SET_NULL, null = True)
    address = models.ForeignKey(to = Address, on_delete = models.SET_NULL, null = True)
    delivery = models.ForeignKey(to = Delivery, on_delete = models.SET_NULL, null = True)

class Review(models.Model):

    review_id = models.PositiveIntegerField(primary_key = True)
    user = models.ForeignKey(to = User, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(to = Order, on_delete = models.SET_NULL, null = True)
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    content_object = GenericForeignKey()
    object_id = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    when = models.DateTimeField(auto_now = True)
    review = models.TextField()

class Payment(models.Model):

    PAYMENT_MODES = ["personal", "mercpago", "neteller", "skrill", "uala"]
    PAYMENT_DEF = PAYMENT_MODES[0]
    PAYMENT_MODES = list(zip(PAYMENT_MODES, PAYMENT_MODES))

    payment_id = models.PositiveIntegerField(primary_key = True)
    when = models.DateTimeField()
    order = models.OneToOneField(to = Order, on_delete = models.SET_NULL, null = True)
    payment_mode = models.CharField(choices = PAYMENT_MODES, default = PAYMENT_DEF, max_length = 8)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, validators = price)

class Coupon(models.Model):

    LIMIT_BASES = ["times", "day", "week", "month"]
    LIMIT_BASES_DEF = LIMIT_BASES[0]
    LIMIT_BASES = list(zip(LIMIT_BASES, LIMIT_BASES))

    coupon_id = models.PositiveIntegerField(primary_key = True, default = 123456789)
    limit_uses = models.PositiveIntegerField(default = 1)
    limit_basis = models.CharField(choices = LIMIT_BASES, default = LIMIT_BASES_DEF, max_length = 5)
    expires = models.DateField(null = True)
    discount = models.JSONField()
