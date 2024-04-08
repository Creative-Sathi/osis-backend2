from django.db import models
from profileseller.models import Seller
from sellerdashboard.models import productinfo

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    dateandtime = models.DateTimeField(auto_now_add=True)
    requested_seller_id = models.ForeignKey('profileseller.Seller', on_delete=models.CASCADE)
    remaining_balance = models.FloatField(null=True,blank=True,default=0.0)

# Model named Quotation that has it's id as Primary key and ID of Seller_quotation as Foreign Key
class Quotation(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    part_id = models.ForeignKey('admindashboard.partinfo', on_delete=models.CASCADE)
    seller_quotation = models.ForeignKey('SpecificSellerQuotation', on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField()
    quantity = models.IntegerField(null=True,blank=True)

# Model named Seller_quotation that has it's id as Primary key  and Order Id as Foreign KEy and Quoted Price
class SpecificSellerQuotation(models.Model):
    id = models.AutoField(primary_key=True)
    quotation_id = models.ForeignKey('Quotation', on_delete=models.CASCADE)
    quoted_seller_id = models.ForeignKey('profileseller.Seller', on_delete=models.CASCADE)
    status = models.CharField()
    quoted_price_per_unit = models.FloatField(blank=True,null=True)
    quoted_price_total  = models.FloatField(blank=True,null=True)
    delivery_period = models.CharField(blank=True,null=True)
    remarks = models.CharField(blank=True,null=True)
    
class UnidentifiedProduct(models.Model):
    partNumber = models.CharField()
    partName = models.CharField()
    partCategories = models.CharField()
    vehicleCompany = models.CharField()
    brand = models.CharField()
    model = models.CharField()
    quantity = models.IntegerField(default=0)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    status = models.CharField(default="Pending")