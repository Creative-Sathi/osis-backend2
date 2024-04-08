from rest_framework import serializers
from profileseller.models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']
        


class SellerProfileSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(many=True, read_only=True, source='company_set')
    companies = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    class Meta:
        model = SellerProfile
        fields = '__all__'
        
    def create(self, validated_data):
        companies_data = validated_data.pop('companies', [])  # Extract companies data
        seller_profile = SellerProfile.objects.create(**validated_data)
        # Iterate over the list of company names and create Company objects
        for company_name in companies_data:
            Company.objects.create(seller_profile=seller_profile, name=company_name)

        return seller_profile
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        
class SellerAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    pickupaddress = AddressSerializer()
    deliveryaddress = AddressSerializer()
    
    class Meta:
        model = SellerAddress
        fields = '__all__'
        
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        pickupaddress_data = validated_data.pop('pickupaddress')
        deliveryaddress_data = validated_data.pop('deliveryaddress')

        address = Address.objects.create(**address_data)
        pickupaddress = Address.objects.create(**pickupaddress_data)
        deliveryaddress = Address.objects.create(**deliveryaddress_data)

        # Create the SellerAddress instance with the Address objects
        seller_address = SellerAddress.objects.create(
            address=address,
            pickupaddress=pickupaddress,
            deliveryaddress=deliveryaddress,
            **validated_data
        )

        return seller_address

class DocumentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentImage
        fields = ['image']
        
class DocumentsSerializer(serializers.ModelSerializer):
    businessdocuments = DocumentImageSerializer(many=True, read_only=True, source='documentimage_set')
    businessdocuments = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    class Meta:
        model = Documents
        fields = '__all__'
    
    def create(self, validated_data):
        businessdocuments_data = validated_data.pop('businessdocuments', [])
        documents = Documents.objects.create(**validated_data)
        for business in businessdocuments_data:
            DocumentImage.objects.create(document=documents, image=business)
            
        return documents
        
        
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
        
class GetAllSellerSerializer(serializers.ModelSerializer):
    sellerprofile = SellerProfileSerializer()
    selleraddress = SellerAddressSerializer()
    documents = DocumentsSerializer()
    
    class Meta:
        model = Seller
        fields = '__all__'
        
    def to_representation(self, instance):
        # Access the related companies through the correct related name (replace 'company_set' with your actual related name)
        companies = instance.sellerprofile.company_set.all()
        businessdocuments = instance.documents.documentimage_set.all()

        # Use the default to_representation implementation and add companies to the serialized data
        representation = super().to_representation(instance)
        representation['sellerprofile']['companies'] = CompanySerializer(companies, many=True).data
        representation['documents']['businessdocuments'] = DocumentImageSerializer(businessdocuments, many=True).data

        return representation