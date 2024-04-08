from django.db import models
import os
from uuid import uuid4
from admindashboard.models import *
from profileseller.models import *

def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = str(uuid4())
    unique_filename = f"{unique_id}.{ext}"
    return os.path.join('uploads/productimages', unique_filename)


class productinfo(models.Model):
    part_id = models.ForeignKey(partinfo,on_delete=models.CASCADE,related_name="Part",null=True,blank=True)
    normalRate = models.CharField()
    bulkRate = models.CharField(blank=True, null=True)
    stockQuantity = models.CharField()
    units = models.CharField()
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name='products')
    status = models.CharField()
  
class reviewproductinfo(models.Model):
    part_id = models.CharField()
    normalRate = models.CharField()
    bulkRate = models.CharField(blank=True, null=True)
    stockQuantity = models.CharField()
    units = models.CharField()
    seller_id = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name='reviewproducts')
    status = models.CharField(default="Reviewed")
  
class productimage(models.Model):
    product = models.ForeignKey(productinfo, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to=unique_filename,blank=True)

class producttags(models.Model):
    product = models.ForeignKey(productinfo, on_delete=models.CASCADE,related_name='tags')
    tagname = models.CharField(blank=True ,null=True)
    
    class Meta:
        unique_together = ('product', 'tagname',)
    
