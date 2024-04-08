# your_app_name/serializers.py
from rest_framework import serializers
from quotation.models import *
from admindashboard.serializers import *
from sellerdashboard.serializers import *
from profileseller.serializers import *

class OrderSerializer(serializers.ModelSerializer):
    requested_seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

    class Meta:
        model = Order
        fields = '__all__'
    
class SpecificSellerQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificSellerQuotation
        fields = '__all__'        
 
class ReadingQuotationSerializer(serializers.ModelSerializer):
    part_id = partinfoSerializer()
    order_id = OrderSerializer()
    
    
    seller_quotation = SpecificSellerQuotationSerializer(required=False, allow_null=True)
    
    class Meta:
        model = Quotation
        fields = '__all__'
        


class QuotationSerializer(serializers.ModelSerializer):
    part_id = serializers.PrimaryKeyRelatedField(queryset=partinfo.objects.all())
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    
    
    seller_quotation = SpecificSellerQuotationSerializer(required=False, allow_null=True)
    
    class Meta:
        model = Quotation
        fields = '__all__'
        
class ReadingSpecificSellerQuotationSerializer(serializers.ModelSerializer):
    quotation_id = ReadingQuotationSerializer()
    class Meta:
        model = SpecificSellerQuotation
        fields = '__all__'
        
class ReadingUnidentifiedProductSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()
    class Meta:
        model = UnidentifiedProduct
        fields = '__all__'
        
        
class UnidentifiedProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UnidentifiedProduct
        fields = '__all__'


