from rest_framework import serializers
from .models import *
from sellerdashboard.serializers import ReadproductinfoSerializer
from admindashboard.serializers import partinfoSerializer

class FeaturedProductSerializer(serializers.ModelSerializer):
    product_id = ReadproductinfoSerializer(read_only=True)
    
    class Meta:
        model = FeaturedProduct
        fields = '__all__'
        

class CategoryCountSerializer(serializers.Serializer):
    partCategories = serializers.CharField()
    product_count = serializers.IntegerField()
    
class TopCarMakerSerializer(serializers.Serializer):
    brand = serializers.CharField()
    product_count = serializers.IntegerField()
    
class LatestProductSerializer(serializers.ModelSerializer):
    part_id = partinfoSerializer(read_only=True)
    part_numbers = serializers.SerializerMethodField()
    
    class Meta:
        model = productinfo
        fields = '__all__'
        
    def get_part_numbers(self, obj):
        part_numbers = obj.part_id.partnumbers.all()
        return [part_number.partNumber for part_number in part_numbers]