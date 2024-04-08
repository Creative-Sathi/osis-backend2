from rest_framework import serializers
from admindashboard.models import *
from sellerdashboard.models import *
from sellerdashboard.serializers import productimageSerializer,producttagsSerializer
from admindashboard.serializers import partinfoSerializer
from .models import *

class searchedproductserializer(serializers.ModelSerializer):
    
    class Meta:
        model = partinfo
        fields = '__all__'
        
class productinfoSerializer(serializers.ModelSerializer):
    images = productimageSerializer(many = True,read_only=True)
    tags = producttagsSerializer(many=True,read_only=True)
    part_id = partinfoSerializer(read_only=True)
    
    class Meta:
        model = productinfo
        fields = '__all__'
        
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = productinfoSerializer(read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        

