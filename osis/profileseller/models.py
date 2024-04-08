from django.db import models
import os
from uuid import uuid4
from django.conf import settings

def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = str(uuid4())
    unique_filename = f"{unique_id}.{ext}"
    return os.path.join('uploads/sellerlogo', unique_filename)


#Model named seller address that has storename, storeemail, storephone, storetype, storewebsite, storelogo, store description
class SellerProfile(models.Model):
    storename = models.CharField()
    storeemail = models.EmailField()
    storephone = models.CharField()
    storetype = models.CharField()
    storewebsite = models.CharField(blank=True, null=True)
    storelogo = models.ImageField(upload_to= unique_filename, blank=True, null=True)
    storedescription = models.TextField()
  
class Company(models.Model):
    name = models.CharField(max_length=255)
    seller_profile = models.ForeignKey(SellerProfile,on_delete=models.CASCADE)

class Address(models.Model):
    address = models.CharField()
    province = models.CharField()
    area = models.CharField()
    district = models.CharField()
    additionalphone = models.CharField()
    descriptiveaddress = models.CharField()
    
    
class SellerAddress(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='business_address')
    pickupaddress = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='pickup_address')
    deliveryaddress = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='delivery_address')
    

class Documents(models.Model):
    ownername = models.CharField(max_length=255)
    businessregdnumber = models.CharField(max_length=255)
    bankdocument = models.ImageField(upload_to=unique_filename)
 
class DocumentImage(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=unique_filename)
   
class Seller(models.Model):
    sellerprofile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='seller_profile')
    selleraddress = models.ForeignKey(SellerAddress, on_delete=models.CASCADE, related_name='seller_address')
    documents = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='seller_documents')
    status = models.CharField(default='Pending')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    remarks = models.CharField(blank=True, null=True)
