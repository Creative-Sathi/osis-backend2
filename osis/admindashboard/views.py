from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework import status
from django.db.models import Q
from rest_framework import viewsets
from admindashboard.serializers import *
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import pandas as pd
import os
import tablib
from admindashboard.models import *
from rest_framework import generics
import base64
from PIL import Image
from io import BytesIO
from django.core.files import File
from openpyxl import load_workbook
from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from sellerdashboard.models import productinfo
from sellerdashboard.serializers import productinfoSerializer, productimageSerializer, producttagsSerializer,ReadproductinfoSerializer
# Create your views here.
from homepage.models import FeaturedProduct
from homepage.serializers import FeaturedProductSerializer
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import zipfile


class PartinfoView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        partinfo_data = request.data
        partnumbers = partinfo_data.getlist('partNumbers[]')
        partinfo_data.pop('partNumbers[]')
        partinfo_data.setlist('partNumber', partnumbers)
        other_attributes_data = []  # List to store the transformed data

        # Iterate through the keys in the data dictionary
        for key in partinfo_data.keys():
            if key.startswith('otherAttributes[') and key.endswith('][attributeValue]'):
                # Extract the index from the key
                index = key.split('[')[1].split(']')[0]
                # Use the index to get the corresponding attributeName and attributeValue
                attribute_value_list = partinfo_data.get(f'otherAttributes[{index}][attributeValue]')
                attribute_key_list = partinfo_data.get(f'otherAttributes[{index}][attributeName]')
                # Check if both attributeName and attributeValue are not empty
                if attribute_value_list:
                    attribute_value = attribute_value_list
                    attribute_key = attribute_key_list
                    other_attributes_data.append({'attributeName': attribute_key , 'attributeValue': attribute_value})
        # Create a dictionary with the transformed data
        transformed_data = {'otherAttributes': other_attributes_data}
        # Merge the transformed_data back into the original data
        partinfo_data.update(transformed_data)
        serializer = partinfoSerializer(data=partinfo_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Part added Sucessfullly'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApprovedPartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        partinfo_queryset = partinfo.objects.filter(status="Approved")
        attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
        partnumber_queryset = partNumber.objects.filter(part__in=partinfo_queryset)
        partinfo_serializer = partinfoSerializer(partinfo_queryset, many=True)
        partinfo_data = partinfo_serializer.data
        attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
        partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True)
        attributes_data = attributes_serializer.data
        partnumber_data = partnumber_serializer.data
        combined_data = []
        

        for partinfo_item in partinfo_data:
            partinfo_id = partinfo_item['id']
            partinfo_item['attributes'] = [attr for attr in attributes_data if attr['part'] == partinfo_id]
            partinfo_item['partNumber'] = [partnum for partnum in partnumber_data if partnum['part'] == partinfo_id]
            combined_data.append(partinfo_item)

        return Response(combined_data)


class CSVPartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        partinfo_queryset = partinfo.objects.filter(status="CSV Added")
        attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
        partnumber_queryset = partNumber.objects.filter(part__in=partinfo_queryset)
        partinfo_serializer = partinfoSerializer(partinfo_queryset, many=True)
        partinfo_data = partinfo_serializer.data
        attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
        partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True)
        attributes_data = attributes_serializer.data
        partnumber_data = partnumber_serializer.data
        combined_data = []

        for partinfo_item in partinfo_data:
            partinfo_id = partinfo_item['id']
            partinfo_item['attributes'] = [attr for attr in attributes_data if attr['part'] == partinfo_id]
            partinfo_item['partNumber'] = [partnum for partnum in partnumber_data if partnum['part'] == partinfo_id]
            combined_data.append(partinfo_item)

        return Response(combined_data)

    
class SellerAddedPartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        partinfo_queryset = partinfo.objects.filter(status="SellerAdded")
        attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
        partnumber_queryset = partNumber.objects.filter(part__in=partinfo_queryset)
        partinfo_serializer = partinfoSerializer(partinfo_queryset, many=True)
        partinfo_data = partinfo_serializer.data
        attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
        partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True)
        attributes_data = attributes_serializer.data
        partnumber_data = partnumber_serializer.data
        combined_data = []

        for partinfo_item in partinfo_data:
            partinfo_id = partinfo_item['id']
            partinfo_item['attributes'] = [attr for attr in attributes_data if attr['part'] == partinfo_id]
            partinfo_item['partNumber'] = [partnum for partnum in partnumber_data if partnum['part'] == partinfo_id]
            combined_data.append(partinfo_item)

        return Response(combined_data)
    

class DeletedPartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        partinfo_queryset = partinfo.objects.filter(status="Deleted")
        attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
        partnumber_queryset = partNumber.objects.filter(part__in=partinfo_queryset)
        partinfo_serializer = partinfoSerializer(partinfo_queryset, many=True)
        partinfo_data = partinfo_serializer.data
        attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
        partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True)
        attributes_data = attributes_serializer.data
        partnumber_data = partnumber_serializer.data
        combined_data = []
        

        for partinfo_item in partinfo_data:
            partinfo_id = partinfo_item['id']
            partinfo_item['attributes'] = [attr for attr in attributes_data if attr['part'] == partinfo_id]
            partinfo_item['partNumber'] = [partnum for partnum in partnumber_data if partnum['part'] == partinfo_id]
            combined_data.append(partinfo_item)

        return Response(combined_data)
    
# View to Update status of given formData
class UpdatePartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        partinfo_data = request.data
        partinfo_id = partinfo_data['partinfo_id']
        updatestatus = partinfo_data['status']
        print("UPDATE STATUS",updatestatus)
        try:
            part_info = partinfo.objects.get(pk = partinfo_id)
            vehicle_company = part_info.vehicleCompany
            brand = part_info.brand
            model = part_info.model
            manufacture_year = part_info.manufactureYear
            subcategory = part_info.partSubCategories
            current_status = part_info.status

            # Assuming partNumber is a related model, use related_name to access part numbers
            part_numbers = part_info.partnumbers.all()
            # If you want to get a list of part numbers as strings, you can use list comprehension
            part_number_list = [part_number.partNumber for part_number in part_numbers]
            
            for part_number in part_number_list:
                found_part = partNumber.objects.filter(partNumber=part_number).first()
                if found_part: 
                    if updatestatus != "Deleted":      
                        if found_part.part.vehicleCompany == vehicle_company and found_part.part.brand == brand and found_part.part.model == model and found_part.part.manufactureYear == manufacture_year and found_part.part.status == "Approved" and found_part.part.partSubCategories == subcategory:
                            return HttpResponse("Partinfo already found", status=404)

            
            part_info.attributes.all().delete()
            part_info.partnumbers.all().delete()
            partinfo_data = request.data.copy()
            
            other_attributes_data = [] 
            for key in partinfo_data.keys():
                if key.startswith('otherAttributes[') and key.endswith('][attributeValue]'):
                    index = key.split('[')[1].split(']')[0] 
                    # Use the index to get the corresponding attributeName and attributeValue
                    attribute_value_list = partinfo_data.get(f'otherAttributes[{index}][attributeValue]')
                    attribute_key_list = partinfo_data.get(f'otherAttributes[{index}][attributeName]')
                    # Check if both attributeName and attributeValue are not empty
                    if attribute_value_list:
                        attribute_value = attribute_value_list
                        attribute_key = attribute_key_list
                        other_attributes_data.append({'attributeName': attribute_key , 'attributeValue': attribute_value})
                        
            # Create a dictionary with the transformed data
            transformed_data = {'otherAttributes': other_attributes_data}
            partinfo_data.update(transformed_data)
            print("WENT FOR SERIALIZER")
            serializer = partinfoSerializer(part_info, data=partinfo_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e),}, status=status.HTTP_404_NOT_FOUND)

class UndoPartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        partinfo_data = request.data
        partinfo_id = partinfo_data['partinfo_id']
        updatestatus = partinfo_data['status']
        try:
            part_info = partinfo.objects.get(pk = partinfo_id)
            vehicle_company = part_info.vehicleCompany
            brand = part_info.brand
            model = part_info.model
            manufacture_year = part_info.manufactureYear

            # Assuming partNumber is a related model, use related_name to access part numbers
            part_numbers = part_info.partnumbers.all()
            # If you want to get a list of part numbers as strings, you can use list comprehension
            part_number_list = [part_number.partNumber for part_number in part_numbers]
            
            for part_number in part_number_list:
                found_part = partNumber.objects.filter(partNumber=part_number).first()
                if found_part: 
                    print("UPDATE STATUS",updatestatus)
                    if updatestatus != "Deleted":      
                        if found_part.part.vehicleCompany == vehicle_company and found_part.part.brand == brand and found_part.part.model == model and found_part.part.manufactureYear == manufacture_year and found_part.part.status == "Approved":
                            return HttpResponse("Partinfo already found", status=404)

            
            part_info.attributes.all().delete()
            part_info.partnumbers.all().delete()
            partinfo_data = request.data.copy()
            
            other_attributes_data = [] 
            for key in partinfo_data.keys():
                if key.startswith('otherAttributes[') and key.endswith('][attributeValue]'):
                    index = key.split('[')[1].split(']')[0] 
                    # Use the index to get the corresponding attributeName and attributeValue
                    attribute_value_list = partinfo_data.get(f'otherAttributes[{index}][attributeValue]')
                    attribute_key_list = partinfo_data.get(f'otherAttributes[{index}][attributeName]')
                    # Check if both attributeName and attributeValue are not empty
                    if attribute_value_list:
                        attribute_value = attribute_value_list
                        attribute_key = attribute_key_list
                        other_attributes_data.append({'attributeName': attribute_key , 'attributeValue': attribute_value})
                        
            # Create a dictionary with the transformed data
            transformed_data = {'otherAttributes': other_attributes_data}
            partinfo_data.update(transformed_data)
            partinfo_data['status'] = updatestatus
            serializer = partinfoSerializer(part_info, data=partinfo_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e),}, status=status.HTTP_404_NOT_FOUND)
    

class DeletePartInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self,request,format = None):
        partinfo_data = request.data
        partinfo_id = partinfo_data['partinfo_id']
        partinfo.objects.filter(id=partinfo_id).delete()
        return Response({'msg':'Part Deleted Sucessfullly'})


# View to add Part from CSV 
class AddPartFromCSVView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)
    
    def post(self,request,format = None):
        partinfo_data = request.data
        print(partinfo_data)
        partinfo_serializer = partinfoSerializer(data=partinfo_data)
        if partinfo_serializer.is_valid():
            partinfo_serializer.save()
            return Response({'msg':'Part added Sucessfullly'}, status=status.HTTP_201_CREATED)
        return Response(partinfo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadPartInfoView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')

        try:
            df = pd.read_excel(file)
            df['status'] = 'CSV Added'
            serialized_data = partinfoCSVSerializer(data=df.to_dict(orient='records'), many=True)
            if serialized_data.is_valid():
                parts = serialized_data.save()
                attribute_columns = ['Remarks']
                partnumber_column = ['partNumber']

                for part, (_, attributes_data), (_, part_numbers) in zip(parts, df[attribute_columns].iterrows(), df[partnumber_column].iterrows()):
                    for attribute_name, attribute_value in attributes_data.items():
                        partAttribute.objects.create(
                            part=part,
                            attributeName=attribute_name,
                            attributeValue=attribute_value
                        )
                    
                    for part_number in part_numbers:
                        partNumber.objects.create(
                            part=part,
                            partNumber=part_number
                        )



                return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serialized_data.errors,}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdatePartView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self,request,format = None):
        partinfo_data = request.data
        partinfo_id = partinfo_data['partinfo_id']
        # Update the whole partinfo object that has partinfo_id using serializer
        
        
        return Response({'msg':'Part Updated Sucessfullly'})
    

class PartinfoAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, pk):
        try:
            part_info = partinfo.objects.get(pk=pk)
            partinfo_data = partinfo
            partnumbers = partinfo_data.getlist('partNumbers[]')
            partinfo_data.pop('partNumbers[]')
            partinfo_data.setlist('partNumber', partnumbers)
            other_attributes_data = []             
            for key in partinfo_data.keys():
                if key.startswith('otherAttributes[') and key.endswith('][attributeValue]'):
                    index = key.split('[')[1].split(']')[0]
                    attribute_name_list = partinfo_data.get(f'otherAttributes[{index}][attributeName]')
                    attribute_value_list = partinfo_data.get(f'otherAttributes[{index}][attributeValue]')
                    if attribute_value_list:
                        attribute_name = attribute_name_list
                        attribute_value = attribute_value_list
                        other_attributes_data.append({'id':index,'attributeName': attribute_name, 'attributeValue': attribute_value})
            transformed_data = {'otherAttributes': other_attributes_data}
            # Merge the transformed_data back into the original data
            partinfo_data.update(transformed_data)
            print(partinfo_data)
            serializer = partinfoSerializer(data=partinfo_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Part added Sucessfullly'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except partinfo.DoesNotExist:
            return Response({"error": "Partinfo not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            part_info = partinfo.objects.get(pk=pk)
            part_info.attributes.all().delete()
            part_info.partnumbers.all().delete()
            partinfo_data = request.data.copy()
            partnumbers = partinfo_data.getlist('partNumbers[]')
            partinfo_data.pop('partNumbers[]')
            partinfo_data.setlist('partNumber', partnumbers)
            
            other_attributes_data = [] 
            for key in partinfo_data.keys():
                if key.startswith('otherAttributes[') and key.endswith('][attributeValue]'):
                    index = key.split('[')[1].split(']')[0] 
                    # Use the index to get the corresponding attributeName and attributeValue
                    attribute_value_list = partinfo_data.get(f'otherAttributes[{index}][attributeValue]')
                    attribute_key_list = partinfo_data.get(f'otherAttributes[{index}][attributeName]')
                    # Check if both attributeName and attributeValue are not empty
                    if attribute_value_list:
                        attribute_value = attribute_value_list
                        attribute_key = attribute_key_list
                        other_attributes_data.append({'attributeName': attribute_key , 'attributeValue': attribute_value})
                        
            # Create a dictionary with the transformed data
            transformed_data = {'otherAttributes': other_attributes_data}
            partinfo_data.update(transformed_data)
            serializer = partinfoSerializer(part_info, data=partinfo_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except partinfo.DoesNotExist:
            return Response({"error": "Partinfo not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            part_info = partinfo.objects.get(pk=pk)
            part_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except partinfo.DoesNotExist:
            return Response({"error": "Partinfo not found"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([AllowAny])
def CompanyInfoView(request):
    company = partinfo.objects.values('vehicleCompany').distinct()
    company_list = [entry['vehicleCompany'] for entry in company]
    return JsonResponse(company_list,safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def BrandInfoView(request,company):
    brand = partinfo.objects.filter(vehicleCompany=company).values('brand').distinct()
    brand_list = [entry['brand'] for entry in brand]
    return JsonResponse(brand_list,safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def ModelInfoView(request,company,brand):
    model = partinfo.objects.filter(vehicleCompany=company,brand=brand).values('model').distinct()
    model_list = [entry['model'] for entry in model]
    return JsonResponse(model_list,safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def PartCategoryView(request):
    partcategory = partinfo.objects.values('partCategories').distinct()
    partcategory_list = [entry['partCategories'] for entry in partcategory if entry['partCategories'] is not None]
    return JsonResponse(partcategory_list, safe=False)

class ApprovedProductInfoView(APIView):
    permission_classes=(AllowAny,)
    
    def get(self, request, format=None):
        product_details = productinfo.objects.filter(status='Approved')
        product_details_data = productinfoSerializer(product_details, many=True, context={'view': self}).data
        for product_details in product_details_data:
            if product_details:
                part_id_value = product_details.get('part_id', {}).get('id', None)
                attributes_queryset = partAttribute.objects.filter(part=part_id_value)
                partnumber_queryset = partNumber.objects.filter(part=part_id_value)
                attributes_serializer = partAttributeSerializer(attributes_queryset, many=True).data
                partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True).data
                product_details['part_id']['attributes'] = attributes_serializer
                product_details['part_id']['partnumber'] = partnumber_serializer

        return Response({'status': 'Success', 'data': product_details_data})
        
class MakeFeaturedProduct(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        try:
            product_id = int(kwargs.get('id'))
            # Get all featured product IDs
            featured_product_ids = FeaturedProduct.objects.values_list('product_id', flat=True)

            # Exclude already featured products and get the product
            product = productinfo.objects.filter(
                ~Q(id__in=featured_product_ids),  # Exclude already featured products
                id=product_id,
                status="Approved"
            ).first()
            if product:
                featuredproduct = FeaturedProduct.objects.create(product_id=product)
                featuredproduct.save()
                return Response({'msg': 'Product added to Featured Successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': 'Could not add to Featured Product'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': 'Product not found', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListFeaturedProduct(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        featured_products = FeaturedProduct.objects.all()
        print(featured_products)
        result_data = []

        for featured_product_instance in featured_products:
            
            id = featured_product_instance.product_id.id
            print("Id",id)
            product_info_instance = productinfo.objects.get(id=id)
          
            if product_info_instance:
                # Serialize product_info_instance and add it to the featured_product_instance data
                product_info_data = productinfoSerializer(product_info_instance,context={'view': self}).data
                featured_product_instance_data = FeaturedProductSerializer(featured_product_instance).data
                featured_product_instance_data['product_info'] = product_info_data
        
                # Add attributes and partnumber data as you did in your existing code
                part_id_value = product_info_instance.part_id.id
                attributes_queryset = partAttribute.objects.filter(part=part_id_value)
                partnumber_queryset = partNumber.objects.filter(part=part_id_value)
                attributes_serializer = partAttributeSerializer(attributes_queryset, many=True).data
                partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True).data
                featured_product_instance_data['attributes'] = attributes_serializer
                featured_product_instance_data['partnumber'] = partnumber_serializer

                # Append the combined data to the result list
                result_data.append(featured_product_instance_data)

        return Response({'status': 'Success', 'data': result_data})


class RemoveFeaturedProduct(APIView):
    permission_classes = (AllowAny,)
    def delete(self, request, *args, **kwargs):
        try:
            product_id = int(kwargs.get('id'))
            product = productinfo.objects.get(id=product_id, status="Approved")
            featuredproduct = FeaturedProduct.objects.get(product_id=product)
            featuredproduct.delete()
            return Response({'msg': 'Product removed from Featured Successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': 'Product not found', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AllCreditView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        credits = Credit.objects.all()
        credit_data = CreditSerializer(credits, many=True, context={'view': self}).data
        return Response({'status': 'Success', 'data': credit_data})
    
class UpdateCreditView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        try:
            credit_data = request.data
            seller_id = credit_data['seller_id']
            credit_provided = credit_data['creditProvided']
            balance = credit_data['currentBalance']
            credit_added = datetime.now()
            balance_updated = datetime.now()
            # credit_used = credit_data['credit_used']
            seller = Seller.objects.get(id=seller_id)
            credit = Credit.objects.get(seller_profile=seller)
            if credit.credit_provided != credit_provided:
                credit.balance = int(credit_provided) + int(balance) - int(credit.credit_provided)
            credit.credit_provided = credit_provided

            credit.credit_added = credit_added
            credit.balance_updated = balance_updated
            # credit.credit_used = credit_used
            credit.save()
            return Response({'msg': 'Credit Updated Successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': 'Credit not found', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
  
@csrf_exempt
def upload_folder(request):
    if request.method == 'POST' and request.FILES.get('zipFile'):
        zip_file = request.FILES.get('zipFile')
        destination_folder = os.path.join(settings.MEDIA_ROOT, 'partimages')


        # Ensure the destination folder exists, create if not
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Save the zip file to the destination folder
        with open(os.path.join(destination_folder, zip_file.name), 'wb+') as destination:
            for chunk in zip_file.chunks():
                destination.write(chunk)

        # Extract the contents of the zip file
        with zipfile.ZipFile(os.path.join(destination_folder, zip_file.name), 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

        return JsonResponse({'message': 'Zip folder uploaded and extracted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'No zip folder uploaded'}, status=400)


class UploadFolderView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        folder = request.FILES.get('folder')

        if not folder:
            return Response({'error': 'No folder provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a directory to store the uploaded folder
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'partimages', folder.name)
        os.makedirs(upload_dir, exist_ok=True)

        # Loop through the folder and save its contents
        for item in folder:
            if item.is_dir():
                # Handle subdirectories if needed
                pass
            else:
                with open(os.path.join(upload_dir, item.name), 'wb+') as destination:
                    for chunk in item.chunks():
                        destination.write(chunk)

        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)
      
class partimageview(APIView):
    permission_classes = (AllowAny,)
  
    def get(self, request):
        folder_name = request.query_params.get('folder_name')
        if not folder_name:
            return Response({'error': 'Folder name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'partimages', folder_name)
        if not os.path.exists(folder_path):
            return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)
        
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                images.append(os.path.join('uploads', 'partimages', folder_name, filename))
        
        return Response({'images': images})
    