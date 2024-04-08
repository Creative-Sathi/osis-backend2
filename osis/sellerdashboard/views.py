from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from sellerdashboard.serializers import *
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import pandas as pd
import os
import tablib
from sellerdashboard.models import *
from admindashboard.models import *
from rest_framework import generics
from admindashboard.serializers import *
from rest_framework.response import Response
from rest_framework import status
from admindashboard.views import ApprovedPartInfoView
from users.models import Order as UserOrder
from users.models import Cart, CartItem
from quotation.models import Order as SellerOrder
from quotation.models import Quotation,SpecificSellerQuotation
from profileseller.models import *
from admindashboard.models import Credit
# # Create your views here.


class ProductinfoView(APIView):
    permission_classes = (IsAuthenticated,)
        
    def post(self, request, format=None):
        user_id = request.user.id
        seller_id = Seller.objects.get(seller=user_id).id
        user_data = request.data.copy()
        part_id = user_data.get('part_id')
        print("Part ID: ", part_id)
        check_product = productinfo.objects.filter(part_id=part_id,seller_id=seller_id,status='Approved')
        
        if check_product.exists():
            return Response({'msg':'Product already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            otherphotos = user_data.getlist('otherPhotos[]')     
            tags = user_data.getlist('tags[]')   
            user_data.setlist('otherPhotos', otherphotos)
            user_data.setlist('tags',tags)
            user_data.pop('otherPhotos[]')
            user_data.pop('tags[]')  
            user_data['seller_id'] = seller_id
            user_data['status'] = 'Approved'
            serializer = productinfoSerializer(data=user_data,context={'view': self})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Product added Sucessfullly'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'Failed to Add Product'},serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EditProductInfoView(APIView):
    permission_classes = (IsAuthenticated,)
        
    def post(self, request, format=None):
        user_id = request.user.id
        seller_id = Seller.objects.get(seller=user_id).id
        user_data = request.data.copy()
        product_id = user_data.get('id')
        print("Part ID: ", product_id)
        print("Seller ID: ", seller_id)
        check_product = productinfo.objects.filter(id=product_id,seller_id=seller_id,status='Approved').first()
        print("Check Product: ", check_product)
        if check_product:
            otherphotos = user_data.getlist('otherPhotos[]')     
            tags = user_data.getlist('tags[]')   
            user_data.setlist('otherPhotos', otherphotos)
            user_data.setlist('tags',tags)
            user_data.pop('otherPhotos[]')
            user_data.pop('tags[]')  
            user_data['seller_id'] = seller_id
            user_data['status'] = 'Approved'
            
            serializer = productinfoSerializer(check_product, data=user_data, context={'view': self}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Product updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Failed to update product', 'errors': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'msg':'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
                  
class RedoProductInfoView(APIView):
    permission_classes = (IsAuthenticated,)
        
    def post(self, request, format=None):
        user_id = request.user.id
        seller_id = Seller.objects.get(seller=user_id).id
        user_data = request.data.copy()
        product_id = user_data.get('productId')
        print("Product ID: ", product_id)
        check_product = productinfo.objects.filter(id=product_id,seller_id=seller_id,status = 'Approved')
        if check_product.exists():
            return Response({'msg':'Product already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            product_object = productinfo.objects.filter(id=product_id,seller_id=seller_id,status="Deleted")
            if product_object.exists():
                product_object.update(status="Approved")
                return Response({'msg':'Product added Sucessfullly'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            
        
class ApprovedProductSpecificInfoView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, format=None):
        user_id = request.user.id
        seller = Seller.objects.get(seller=user_id)
        approved_products = productinfo.objects.filter(status='Approved',seller_id=seller.id)
        product_serializer = productinfoSerializer(approved_products, many=True, context={'view': self})
        data = []
        approved_products_list = list(approved_products)
        for product in approved_products:
            part_data = partinfoSerializer(product.part_id).data
            partinfo_queryset = partinfo.objects.filter(id = product.part_id.id)
            attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
            partnumber_queryset = partNumber.objects.filter(part__in=partinfo_queryset)
            partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True)
            attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
            attributes_data = attributes_serializer.data
            image_data = productimageSerializer(product.images.all(), many=True).data
            tag_data = producttagsSerializer(product.tags.all(), many=True).data
            product_data = product_serializer.data[approved_products_list.index(product)]
            product_data['part_info'] = part_data
            product_data['attributes'] = attributes_data
            product_data['images'] = image_data
            product_data['partnumbers'] = partnumber_serializer.data
            product_data['tags'] = tag_data
            data.append(product_data)
        
        return Response(data, status=status.HTTP_200_OK)

class DeletedProductInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, format=None):
        user_id = request.user.id
        seller = Seller.objects.get(seller=user_id)
        approved_products = productinfo.objects.filter(status='Deleted',seller_id=seller.id)
        product_serializer = productinfoSerializer(approved_products, many=True, context={'view': self})
        data = []
        approved_products_list = list(approved_products)
        for product in approved_products:
            part_data = partinfoSerializer(product.part_id).data
            partinfo_queryset = partinfo.objects.filter(id = product.part_id.id)
            attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
            attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
            attributes_data = attributes_serializer.data
            image_data = productimageSerializer(product.images.all(), many=True).data
            tag_data = producttagsSerializer(product.tags.all(), many=True).data
            product_data = product_serializer.data[approved_products_list.index(product)]
            product_data['part_info'] = part_data
            product_data['attributes'] = attributes_data
            product_data['images'] = image_data
            product_data['tags'] = tag_data
            data.append(product_data)
        
        return Response(data, status=status.HTTP_200_OK)
    
class UpdateProductInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        partinfo_data = request.data
        partinfo_id = partinfo_data['productinfo_id']
        status = partinfo_data['status']
        productinfo.objects.filter(id=partinfo_id).update(status=status)
        return Response({'msg':'Status Updated Sucessfullly'})   

class RemoveProductInfoView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        try:
            partinfo_data = request.data
            partinfo_id = partinfo_data['productId']
            print("Product ID: ", partinfo_id)
            productinfo.objects.filter(id=partinfo_id).delete()
            return Response({'msg':'Product Deleted Sucessfullly'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}','msg':'Failed to Delete Product'}, status=status.HTTP_400_BAD_REQUEST)

class ApprovedProductInfoView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, format=None):
        user_id = request.user.id
        print("USer ID ", user_id)
        seller_profile = Seller.objects.get(seller=user_id)
        approved_products = productinfo.objects.filter(status='Approved').exclude(seller_id=seller_profile.id)
        product_serializer = productinfoSerializer(approved_products, many=True, context={'view': self})
        data = []
        approved_products_list = list(approved_products)
        for product in approved_products:
            part_data = partinfoSerializer(product.part_id).data
            partinfo_queryset = partinfo.objects.filter(id = product.part_id.id)
            attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
            attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
            attributes_data = attributes_serializer.data
            image_data = productimageSerializer(product.images.all(), many=True).data
            tag_data = producttagsSerializer(product.tags.all(), many=True).data
            product_data = product_serializer.data[approved_products_list.index(product)]
            product_data['attributes'] = attributes_data
            product_data['images'] = image_data
            product_data['tags'] = tag_data
            data.append(product_data)
        
        return Response(data, status=status.HTTP_200_OK)

class AgentApprovedProductInfoView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, format=None):
        user_id = request.user
        if user_id.role == "Agent":
            approved_products = productinfo.objects.filter(status='Approved')
            product_serializer = productinfoSerializer(approved_products, many=True, context={'view': self})
            data = []
            approved_products_list = list(approved_products)
            for product in approved_products:
                part_data = partinfoSerializer(product.part_id).data
                partinfo_queryset = partinfo.objects.filter(id = product.part_id.id)
                attributes_queryset = partAttribute.objects.filter(part__in=partinfo_queryset)
                attributes_serializer = partAttributeSerializer(attributes_queryset, many=True)
                attributes_data = attributes_serializer.data
                image_data = productimageSerializer(product.images.all(), many=True).data
                tag_data = producttagsSerializer(product.tags.all(), many=True).data
                product_data = product_serializer.data[approved_products_list.index(product)]
                product_data['attributes'] = attributes_data
                product_data['images'] = image_data
                product_data['tags'] = tag_data
                data.append(product_data)
            
            return Response(data, status=status.HTTP_200_OK)

class UploadProductInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        user = request.user
        seller = Seller.objects.get(seller=user)
        status_value = 'Reviewed'
        part_id_value = None

        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file)

            # Call a URL here to get the part info
            approved_part_info_view = ApprovedPartInfoView()
            response = approved_part_info_view.get(request)

            if response.status_code == status.HTTP_200_OK:
                data = response.data
                for index, row in df.iterrows():
                    part_id = row['part_id']
                    normal_rate = row['normalRate']
                    bulk_rate = row.get('bulkRate', None)
                    stock_quantity = row['stockQuantity']
                    units = row['units']
                    seller_id = seller.id
                    
                    part_id_list = []
                    status_list = []
                    match_found = False
                    
                    
                    # Check if any partNumber matches the part_id
                    for item in data:
                        part_numbers = item.get('partNumber', [])
                        for part_number in part_numbers:
                            if part_number['partNumber'] == part_id:
                                status_value = 'Approved'
                                part_id_value = part_number['part']
                                part_id_list.append(part_id_value)
                                status_list.append(status_value)
                                match_found = True
                                break
                    else:
                        if not match_found:
                            status_value = 'Reviewed'
                            part_id_value = part_id
                            part_id_list.append(part_id_value)
                            status_list.append(status_value)
        

                    if part_id_list and status_list:
                        part_id_list = list(map(str, part_id_list))
                        status_list = list(map(str, status_list))
                        print("Part ID List: ", part_id_list)
                        print("Status List: ", status_list)
                        for part_id_value, status_value in zip(map(str, part_id_list), status_list):
                            if status_value == 'Approved':
                                products_data = productinfo.objects.filter(part_id=int(part_id_value), seller_id=seller_id , status='Approved')
                                if products_data.exists():
                                    quantity = products_data[0].stockQuantity
                                    products_data.update(stockQuantity=int(quantity) + stock_quantity)
                                    products_data.update(normalRate=normal_rate)
                                    products_data.update(bulkRate=bulk_rate)
                                    products_data.update(units=units)
                                else:
                                    product_info = {
                                        'part_id': part_id_value,
                                        'normalRate': normal_rate,
                                        'bulkRate': bulk_rate,
                                        'stockQuantity': stock_quantity,
                                        'units': units,
                                        'seller_id': seller_id,
                                        'status': status_value,
                                    }

                                    product_serializer = productinfoCSVSerializer(data=product_info, context={'request': request})
                                    if product_serializer.is_valid():
                                        product_serializer.save()
                                    else:
                                        return Response({'error': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                                    
                            else:                                             
                                product_info = {
                                    'part_id': part_id_value,
                                    'normalRate': normal_rate,
                                    'bulkRate': bulk_rate,
                                    'stockQuantity': stock_quantity,
                                    'units': units,
                                    'seller_id': seller_id,
                                    'status': status_value,
                                }
                                print("Product Info: ", product_info)

                                review_serializer = reviewproductinfoSerializer(data=product_info)
                                if review_serializer.is_valid():
                                    review_serializer.save()
                                    print("Review Serializer: ", review_serializer.data)
                                else:
                                    return Response({'error': review_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                                

                return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to fetch approved part info'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class ReviewProductInfoView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, format=None):
        user_id = request.user.id
        seller = Seller.objects.get(seller=user_id)
        approved_products = reviewproductinfo.objects.filter(status='Reviewed',seller_id=seller.id)
        product_serializer = reviewproductinfoSerializer(approved_products, many=True)
        data = []

        approved_products_list = list(approved_products)
        
        for product in approved_products_list:
            reviewinfo_queryset = reviewproductinfo.objects.filter(id = product.id)
            product_serializer = reviewproductinfoSerializer(reviewinfo_queryset, many=True)
            product_data = product_serializer.data[0]
            data.append(product_data)
            
        return Response(data, status=status.HTTP_200_OK)

class OrderInfoView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, currentstatus, format=None):
        user_id = request.user.id
        seller = Seller.objects.get(seller=user_id)
        inactive_carts = Cart.objects.filter(is_active=False)
        cartitems = CartItem.objects.filter(product__seller_id=seller.id,cart__in=inactive_carts)
        user_orders = UserOrder.objects.filter(status=currentstatus,cart__in=[cart_item.cart for cart_item in cartitems])
        
        if currentstatus == 'Pending':
            currentstatus = 'Accepted'
        order_id = Quotation.objects.filter(seller_quotation__quoted_seller_id=seller.id, status=currentstatus).values_list('order_id', flat=True)

        seller_orders = SellerOrder.objects.filter(id__in=order_id)
        

        data = []

        for order in seller_orders:
            quotations = Quotation.objects.filter(order_id=order.id, status=currentstatus)
            print("Quotations: ", quotations)
            total_items = 0
            total_price = 0.0
            products = []
            specific_seller_quotations = None

            for quotation in quotations:
                specific_seller_quotations = SpecificSellerQuotation.objects.filter(id=quotation.seller_quotation.id)
                for specific_seller_quotation in specific_seller_quotations:
                    total_items += quotation.quantity
                    total_price += specific_seller_quotation.quoted_price_total or 0.0
                    products.append({
                        'product_name': quotation.part_id.partName,
                        'quantity': quotation.quantity,
                    })
                    
            
            if specific_seller_quotations:
                order_data = {
                    'id': 'B' + str(order.id),
                    'dateandtime': order.dateandtime.strftime('%Y-%m-%d'),
                    'Name': specific_seller_quotations.first().quoted_seller_id.sellerprofile.storename,
                    'phone': specific_seller_quotations.first().quoted_seller_id.sellerprofile.storephone,
                    'Address': str(specific_seller_quotations.first().quoted_seller_id.selleraddress.address),
                    'payment_method': 'Balance',
                    'total_items': total_items,
                    'total_price': total_price,
                    'products': products,
                }
                data.append(order_data)    
        
        for order in user_orders:
            cartdetails = CartItem.objects.filter(cart = order.cart)
            order_data = {
                'id': 'C' + str(order.id),
                'dateandtime': order.date.strftime('%Y-%m-%d'),
                'Name' : order.fullname,
                'phone': order.phone,
                'Address': order.Address,
                'payment_method': order.payment_method,
                'total_items': order.total_items,
                'total_price': order.total_price,
                'products': [{'product_name': item.product.part_id.partName, 'quantity': item.quantity,} for item in cartdetails.all()],
                
            }
            data.append(order_data)
        return Response(data, status=status.HTTP_200_OK)
    
    
class AdminOrderInfoView(APIView):
    permission_classes=(AllowAny,)
    
    def get(self, request, currentstatus, format=None):
        user_orders = UserOrder.objects.filter(status=currentstatus)
        
        order_id = Quotation.objects.filter(status=currentstatus).values_list('order_id', flat=True)

        seller_orders = SellerOrder.objects.filter(id__in=order_id)
        

        data = []

        for order in seller_orders:
            quotations = Quotation.objects.filter(order_id=order.id, status=currentstatus)
            print("Quotations: ", quotations)
            total_items = 0
            total_price = 0.0
            products = []
            specific_seller_quotations = None

            for quotation in quotations:
                specific_seller_quotations = SpecificSellerQuotation.objects.filter(id=quotation.seller_quotation.id)
                for specific_seller_quotation in specific_seller_quotations:
                    total_items += quotation.quantity
                    total_price += specific_seller_quotation.quoted_price_total or 0.0
                    products.append({
                        'product_name': quotation.part_id.partName,
                        'quantity': quotation.quantity,
                    })
                    
            
            if specific_seller_quotations:
                order_data = {
                    'id': 'B' + str(order.id),
                    'dateandtime': order.dateandtime.strftime('%Y-%m-%d'),
                    'Name': specific_seller_quotations.first().quoted_seller_id.sellerprofile.storename,
                    'phone': specific_seller_quotations.first().quoted_seller_id.sellerprofile.storephone,
                    'Address': str(specific_seller_quotations.first().quoted_seller_id.selleraddress.address),
                    'payment_method': 'Balance',
                    'total_items': total_items,
                    'total_price': total_price,
                    'products': products,
                }
                data.append(order_data)    
        
        for order in user_orders:
            cartdetails = CartItem.objects.filter(cart = order.cart)
            order_data = {
                'id': 'C' + str(order.id),
                'dateandtime': order.date.strftime('%Y-%m-%d'),
                'Name' : order.fullname,
                'phone': order.phone,
                'Address': order.Address,
                'payment_method': order.payment_method,
                'total_items': order.total_items,
                'total_price': order.total_price,
                'products': [{'product_name': item.product.part_id.partName, 'quantity': item.quantity,} for item in cartdetails.all()],
                
            }
            data.append(order_data)
        return Response(data, status=status.HTTP_200_OK)
    
class ChangeOrderStatusView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, order_id, newstatus,  format=None):
        try:
            if order_id[0] == 'B':
                order_id= int(order_id[1:])
                seller_order = SellerOrder.objects.get(id=order_id)
                matching_order_quotation = Quotation.objects.filter(order_id=seller_order.id)
                for order_quotation in matching_order_quotation:
                    order_quotation.status = newstatus
                    quoted_seller = SpecificSellerQuotation.objects.get(id=order_quotation.seller_quotation.id)
                    quoted_seller.status = newstatus
                    quoted_seller.save()
                    order_quotation.save()
                    return Response({'msg': 'Status changed successfully'}, status=status.HTTP_200_OK)
            elif order_id[0] == 'C':
                order_id= int(order_id[1:])
                user_order = UserOrder.objects.get(id=order_id)
                user_order.status = newstatus
                user_order.save()
                return Response({'msg': 'Status changed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)        
            
class BalanceDetailsView(APIView):
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, format=None):
        try:
            user_id = request.user.id
            seller = Seller.objects.get(seller=user_id)
            credit = Credit.objects.get(seller_profile=seller.id)
            data = {
                'credit_provided': credit.credit_provided,
                'balance': credit.balance,
                'credit_added': credit.credit_added,
                'balance_updated': credit.balance_updated,
                'credit_used': credit.credit_used,
                
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)