from django.db import models
from authentication.models import User
from sellerdashboard.models import productinfo as Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Changed from product_id to product

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    is_active = models.BooleanField(default=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    total_items = models.PositiveIntegerField()
    total_price = models.FloatField()
    status = models.CharField(max_length=255, default='Pending')
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    return_status = models.CharField(blank=True, null=True, max_length=255)