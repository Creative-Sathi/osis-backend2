from django.db import models
import os
from uuid import uuid4
from profileseller.models import Seller
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = str(uuid4())
    unique_filename = f"{unique_id}.{ext}"
    return os.path.join('uploads/productimages', unique_filename)

class partimages(models.Model):
    image = models.ImageField(upload_to='uploads/partimages/')
    
class partinfo(models.Model):
    vehicleCompany = models.CharField()
    subCategory = models.CharField()
    brand = models.CharField()
    model = models.CharField()
    manufactureYear = models.CharField()    
    partCategories = models.CharField(blank=True ,null=True)
    partSubCategories = models.CharField()
    partName = models.CharField()
    description = models.TextField(blank=True ,null=True)
    availability = models.CharField(default="In Stock")
    image = models.ImageField(upload_to=unique_filename,blank=True,null=True,default='uploads/partimages/default.jpg')
    status = models.CharField()
    
class partNumber(models.Model):
    part = models.ForeignKey(partinfo, on_delete=models.CASCADE,related_name='partnumbers')
    partNumber = models.CharField()

class partAttribute(models.Model):
    part = models.ForeignKey(partinfo, on_delete=models.CASCADE,related_name='attributes')
    attributeName = models.CharField(blank=True ,null=True)
    attributeValue = models.CharField(blank=True ,null=True)
    
class partimage(models.Model):
    part = models.ForeignKey(partinfo, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to=unique_filename,blank=True)
    
class companyimages(models.Model):
    image = models.ImageField(upload_to='uploads/company/')
    
class categoryimages(models.Model):
    image = models.ImageField(upload_to='uploads/category/')

class Credit(models.Model):
    seller_profile =models.ForeignKey(Seller, on_delete=models.CASCADE,related_name='seller_profile')
    credit_provided = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    credit_added = models.DateTimeField(blank=True,null=True)
    balance_updated = models.DateTimeField(blank=True,null=True)
    credit_used = models.DateTimeField(blank=True,null=True)


@receiver(pre_save, sender=Seller)
def create_credit_for_approved_seller(sender, instance, **kwargs):
    if instance.pk:  # Check if instance exists
        old_instance = Seller.objects.get(pk=instance.pk)
        if old_instance.status != 'Approved' and (instance.status == "Approved" or instance.status == "Both" or instance.status == "Buyer" or instance.status == "Seller"):  # Check if status has changed to 'Approved'
            if not Credit.objects.filter(seller_profile=instance).exists():
                Credit.objects.create(seller_profile=instance)