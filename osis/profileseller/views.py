from django.shortcuts import render
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from profileseller.serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class SellerProfileView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request, format=None):
        user_data = request.data.copy()
        
        Companies = user_data.getlist('companies[]')
        user_data.pop('companies[]')
        user_data.setlist('companies', Companies)

        serializer = SellerProfileSerializer(data=user_data)

        if serializer.is_valid():
            seller_profile = serializer.save()
            return Response({'msg':'Seller Profile added Successfully','id':seller_profile.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AddressView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            addressId = serializer.data['id']
            return Response(data =addressId, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
class SellerAddressView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None): 
        serializer = SellerAddressSerializer(data=request.data)
        if serializer.is_valid():
            seller_address = serializer.save()
            return Response({'msg':'Seller Address added Sucessfullly','id':seller_address.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
class DocumentsView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request, format=None):
        user_data = request.data
        businessdocuments = user_data.getlist('businessdocuments[]')
        user_data.pop('businessdocuments[]')
        user_data.setlist('businessdocuments', businessdocuments)
        
        serializer = DocumentsSerializer(data=request.data)
        if serializer.is_valid():
            seller_document = serializer.save()
            return Response({'msg':'Documents added Sucessfullly','id':seller_document.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
class SellerView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            seller = serializer.save()
            return Response({'msg':'Seller added Sucessfullly'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
# View for getting seller profile
class GetSellerProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, format=None): 
        id= request.user.id
        seller = Seller.objects.get(seller=id)
        
        seller_profile = SellerProfile.objects.filter(id=seller.sellerprofile.id)
        serializer = SellerProfileSerializer(seller_profile, many=True)
        return Response(serializer.data)
    

#View for getting all seller
class GetallrequestedSeller(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, format = None):
        all_seller = Seller.objects.filter(status='Pending')
        serializer = GetAllSellerSerializer(all_seller,many=True)
        return Response(serializer.data)
    
#View for Getting all Approved Seller
class GetAllApprovedSeller(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, format = None):
        all_seller = Seller.objects.filter(status__in=['Approved', 'Buyer', 'Seller', 'Both'])
        serializer = GetAllSellerSerializer(all_seller,many=True)
        return Response(serializer.data)
    
#View for Getting all Rejected Seller
class GetAllRejectedSeller(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, format = None):
        all_seller = Seller.objects.filter(status='Rejected')
        serializer = GetAllSellerSerializer(all_seller,many=True)
        return Response(serializer.data)
    
#View for Getting all Seller Details of Particular Seller
class GetAllSpecificSellerDetails(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, format = None):
        user_id = request.user.id        
        all_seller = Seller.objects.filter(seller=user_id)
        serializer = GetAllSellerSerializer(all_seller,many=True)
        return Response(serializer.data)
    
class ManageVendor(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        try:
            seller_id = request.data['seller']
            seller = Seller.objects.get(id=seller_id)
            seller.status = request.data['usertype']
            seller.save()
            return Response({'msg':'Seller added Sucessfullly'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'msg':'Seller not found'}, status=status.HTTP_400_BAD_REQUEST)        
