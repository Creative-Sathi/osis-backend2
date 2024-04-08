from rest_framework import serializers
from sellerdashboard.models import *
from admindashboard.serializers import partinfoSerializer
from users.models import Order as UserOrder
from django.core.exceptions import MultipleObjectsReturned


class productimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = productimage
        fields = ('image',)
        
class producttagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = producttags
        fields = ('tagname',)

class ReadproductinfoSerializer(serializers.ModelSerializer):
    images = productimageSerializer(many = True,read_only=True)
    tags = producttagsSerializer(many=True,read_only=True)
    part_id = partinfoSerializer(read_only=True)
    class Meta:
        model = productinfo
        fields = '__all__'
        
class productinfoSerializer(serializers.ModelSerializer):
    
    images = productimageSerializer(many = True,read_only=True,source='otherPhotos')
    otherPhotos = serializers.ListField(
        child = serializers.ImageField(allow_empty_file=False,use_url=False),
        write_only=True
    )
    
    tags = serializers.ListField(
        child = serializers.CharField(),
        write_only=True
    )
    
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        view_name = context.get('view').__class__.__name__ if context.get('view') else None
        super().__init__(*args, **kwargs)
        
        if view_name != 'ProductinfoView':
            self.fields['part_id'] = partinfoSerializer()
            
    class Meta:
        model = productinfo
        fields = '__all__'
        
    def create(self,validated_data):       
        other_photos = validated_data.pop('otherPhotos')
        tags = validated_data.pop('tags')

        product = productinfo.objects.create(**validated_data)
        
        for image in other_photos:
            productimage.objects.create(product=product,image=image)

        for tag in tags:
            producttags.objects.create(product=product,tagname=tag)

        return product
    
    def update(self, instance, validated_data):
        other_photos = validated_data.pop('otherPhotos', [])
        tags = validated_data.pop('tags', [])

        # Update the productinfo instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle the otherPhotos field
        for image in other_photos:
            productimage.objects.create(product=instance, image=image)
            
        new_tags = set(tags)  # Convert the list of new tags to a set for efficiency
        old_tags = set(tag.tagname for tag in instance.tags.all())  # Get the set of old tags
        
        # Delete the tags that are not in the new tags
        for tag_name in old_tags - new_tags:
            tag = producttags.objects.get(tagname=tag_name, product=instance)
            tag.delete()
        # Handle the tags field
        for tag_name in tags:
            try:
                tag, created = producttags.objects.get_or_create(tagname=tag_name, defaults={'product': instance})
                if not created and tag.product != instance:
                    tag.product = instance
                    tag.save()
            except MultipleObjectsReturned:
                tags = producttags.objects.filter(tagname=tag_name)
                for tag in tags:
                    tag.delete()
        return instance
  
class reviewproductinfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = reviewproductinfo
        fields = '__all__'
    
class productinfoCSVSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = productinfo
        fields = ['part_id','normalRate','bulkRate','stockQuantity','units','seller_id','status']
        
class UserOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserOrder
        fields = '__all__'