from django.db import models
from sellerdashboard.models import productinfo

# Create your models here.
class FeaturedProduct(models.Model):
    product_id = models.ForeignKey(productinfo, on_delete=models.CASCADE,related_name='featuredproducts')
    