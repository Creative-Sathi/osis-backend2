from rest_framework import serializers
from admindashboard.models import *
from profileseller.serializers import GetAllSellerSerializer
                
class partAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = partAttribute
        fields = ('attributeName','attributeValue','part')
        
class partNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = partNumber
        fields = ['partNumber']
        
class partNumberReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = partNumber
        fields = ('partNumber','part')
        
class partinfoSerializer(serializers.ModelSerializer):
    otherAttributes = partAttributeSerializer(many=True,read_only=True, source='attributes')
    otherAttributes = serializers.ListField(
        child=serializers.ListField(
            child=serializers.DictField(
                child=serializers.CharField(),
            )
        ),
        write_only=True
    )
    partNumber = partNumberSerializer(many=True,read_only=True, source='partnumber')
    partNumber = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    class Meta:
        model = partinfo
        fields = '__all__'
        
    def create(self,validated_data):
        other_attributes_data = validated_data.pop('otherAttributes')
        partNumber_data = validated_data.pop('partNumber',[])
        vehicle_company = validated_data.get('vehicleCompany')
        brand = validated_data.get('brand')
        model = validated_data.get('model')
        manufacture_year = validated_data.get('manufactureYear')
        sub_category = validated_data.get('partSubCategories')
        partinfo_id = validated_data.get('partinfo_id')
        # Check if any similar part already exists
        for part_number in partNumber_data:
            
            approved_part_number = partinfo.objects.filter(id = partinfo, status = 'Approved').first()
            if approved_part_number:
                found_part = partNumber.objects.filter(partNumber=part_number).first()
                print(found_part.part.vehicleCompany,found_part.part.brand,found_part.part.model,found_part.part.manufactureYear,found_part.part.partSubCategories,found_part.part.status)
                if found_part:
                    if found_part.part.vehicleCompany == vehicle_company and found_part.part.brand == brand and found_part.part.model == model and found_part.part.manufactureYear == manufacture_year and found_part.part.partSubCategories == sub_category and found_part.part.status == 'Approved':
                        print("Part with the same details already exists")
                        raise ValueError(f"Part with the same details already exists for part number: {part_number}")
            
        part = partinfo.objects.create(**validated_data)
        for item in other_attributes_data:
            for attribute_data  in item:
                partAttribute.objects.create(
                    part=part,
                    attributeName=attribute_data['attributeName'],
                    attributeValue=attribute_data['attributeValue']
                )    
        for partnumbers in partNumber_data:
            partNumber.objects.create(
                part=part,
                partNumber=partnumbers
            )
        return part
    
    def update(self, instance, validated_data):
        other_attributes_data = validated_data.pop('otherAttributes', [])
        partNumber_data = validated_data.pop('partNumber', [])
        vehicle_company = validated_data.get('vehicleCompany')
        brand = validated_data.get('brand')
        model = validated_data.get('model')
        manufacture_year = validated_data.get('manufactureYear')
        sub_category = validated_data.get('partSubCategories')
        # Check if any similar part already exists
        for part_number in partNumber_data:
            print(part_number)
            found_part = partNumber.objects.filter(partNumber=part_number).first()

            if found_part:     
                if found_part.part.vehicleCompany == vehicle_company and found_part.part.brand == brand and found_part.part.model == model and found_part.part.manufactureYear == manufacture_year and found_part.part.partSubCategories == sub_category and found_part.part.status == 'Approved':
                    print("Part with the same details already exists")
                    raise ValueError(f"Part with the same details already exists for part number: {part_number}")

        # Update partinfo instance
        instance.vehicleCompany = validated_data.get('vehicleCompany', instance.vehicleCompany)
        instance.subCategory = validated_data.get('subCategory', instance.subCategory)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)    
        instance.manufactureYear = validated_data.get('manufactureYear', instance.manufactureYear)
        instance.partCategories = validated_data.get('partCategories', instance.partCategories)
        instance.partSubCategories = validated_data.get('partSubCategories', instance.partSubCategories)
        instance.partName = validated_data.get('partName', instance.partName)
        instance.description = validated_data.get('description', instance.description)
        instance.availability = validated_data.get('availability', instance.availability)
        instance.image = validated_data.get('image', instance.image)
        instance.status = validated_data.get('status', instance.status)

        # Save the updated instance
        instance.save()
        found_product = partinfo.objects.get(id=instance.id) 
        # Create new partAttribute instances
        for item in other_attributes_data:
            for attribute_data in item:
                partAttribute.objects.create(
                    part=found_product,
                    attributeName=attribute_data['attributeName'],
                    attributeValue=attribute_data['attributeValue']
                )
                

        # Create new partNumber instances
        for part_number in partNumber_data:
            partNumber.objects.create(
                part=found_product,
                partNumber=part_number
            )
            print(partNumber)

        return instance


class partinfoCSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = partinfo
        fields = '__all__'
        

class CreditSerializer(serializers.ModelSerializer):
    seller_profile = GetAllSellerSerializer(many=False, read_only=True)
    
    class Meta:
        model = Credit
        fields = ('seller_profile','credit_provided','balance','credit_added','balance_updated','credit_used')
        
class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = partimages
        fields = ('image',)