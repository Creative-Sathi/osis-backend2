from admindashboard.models import *
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from sellerdashboard.serializers import *
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import pandas as pd
import os
import tablib
from sellerdashboard.models import *
from .models import *
from rest_framework import generics
from .serializers import *
from django.shortcuts import get_object_or_404
from decimal import Decimal
from admindashboard.serializers import *
from admindashboard.models import *
import json
from django.db.models import Q
import glob

class SearchedProducts(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        search_query = kwargs['search']
        search_terms = search_query.split()  # Split the search query by spaces

        # Initialize the filter criteria
        filter_criteria = {
            'vehicleCompany__icontains': None,
            'brand__icontains': None,
            'manufactureYear__icontains': None,
        }

        # Initialize result queryset
        result = partinfo.objects.filter(status='Approved')

        # Get matching part numbers
        partnumber_matching = partNumber.objects.filter(partNumber__in=search_terms)
        
        print(f"Part Number Matching: {partnumber_matching}")

        if partnumber_matching.exists():
            # Get part IDs from matching part numbers
            partnumber_matching_values = partnumber_matching.values_list('part_id', flat=True)
            # Filter result queryset based on part IDs
            result = result.filter(id__in=partnumber_matching_values)
            
            print(f"Result: {result}")
            
            # Extract category information from matched part numbers
            category_info = result.values_list('brand', 'model', 'manufactureYear').distinct().first()
            if category_info:
                filter_criteria['brand__icontains'] = category_info[0]
                filter_criteria['manufactureYear__icontains'] = category_info[2]
                result = result.filter(brand=category_info[0], model=category_info[1], manufactureYear=category_info[2])
        else:
            # Apply filters based on search terms
            for term in search_terms:
                # Check if term matches vehicleCompany
                if not filter_criteria['vehicleCompany__icontains'] and partinfo.objects.filter(vehicleCompany__icontains=term).exists():
                    filter_criteria['vehicleCompany__icontains'] = term
                    result = result.filter(vehicleCompany__icontains=term)

                # Check if term matches brand
                if not filter_criteria['brand__icontains'] and partinfo.objects.filter(brand__icontains=term).exists():
                    filter_criteria['brand__icontains'] = term
                    result = result.filter(brand__icontains=term)

                # Check if term matches manufactureYear
                if not filter_criteria['manufactureYear__icontains'] and partinfo.objects.filter(manufactureYear__icontains=term).exists():
                    filter_criteria['manufactureYear__icontains'] = term
                    result = result.filter(manufactureYear__icontains=term)

        # Determine which pages to show based on the filter criteria
        pages_to_show = []
        if filter_criteria['vehicleCompany__icontains']:
            pages_to_show = (['SubCategory', 'Brand', 'Year', 'Model'])
        if filter_criteria['brand__icontains']:
            pages_to_show.extend(['SubCategory', 'Year', 'Model'])
        if filter_criteria['manufactureYear__icontains']:
            pages_to_show.extend(['SubCategory', 'Model'])
        if not pages_to_show:
            pages_to_show = ['SubCategory', 'Company', 'Brand', 'Year', 'Model']
        

        # Prepare response
        response_data = {
            'filtered_result': list(result.values()),
            'filter_criteria': filter_criteria,
            'pages_to_show': pages_to_show,
        }

        return Response(response_data)

class SearchedProductsSpecific(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        category = kwargs['category']
        brand = kwargs['brand']
        year = kwargs['year']
        model = kwargs['model']
        result = partinfo.objects.filter(partCategories__icontains=category, brand__icontains=brand, manufactureYear__icontains=year, model__icontains=model, status='Approved')
        result_data = partinfoSerializer(result, many=True).data
        return Response({'status': 'Success', 'data': result_data})
   
class SpecificSearchedProducts(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        search_query = kwargs['id']
        product_details = productinfo.objects.filter(id=search_query, status='Approved')
        product_details_data = productinfoSerializer(product_details, many=True).data
        if product_details_data:
            first_product_details = product_details_data[0]
            part_id_value = first_product_details.get('part_id', {}).get('id', None)
            attributes_queryset = partAttribute.objects.filter(part=part_id_value)
            partnumber_queryset = partNumber.objects.filter(part=part_id_value)
            attributes_serializer = partAttributeSerializer(attributes_queryset, many=True).data
            partnumber_serializer = partNumberReadSerializer(partnumber_queryset, many=True).data
            product_details_data[0]['part_id']['attributes'] = attributes_serializer
            product_details_data[0]['part_id']['partnumber'] = partnumber_serializer
            return Response({'status': 'Success', 'data': product_details_data})
        else:
            return Response({'status': 'Error', 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class SimilarProducts(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        try:
            product_id = kwargs['id']
            product = productinfo.objects.get(id=product_id)
            part_id = product.part_id
            matching_part_numbers = partNumber.objects.filter(part=part_id)
            matching_part_numbers_values = matching_part_numbers.values_list('partNumber', flat=True)
            
            all_part_numbers = partNumber.objects.filter(partNumber__in=matching_part_numbers_values).exclude(part=part_id)
            all_part_ids = all_part_numbers.values_list('part', flat=True)
            
            similar_products = productinfo.objects.filter(part_id__in=all_part_ids, status='Approved')
            similar_products_data = productinfoSerializer(similar_products, many=True).data
            return Response({'status': 'Success', 'data': similar_products_data})
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'status': 'Error', 'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchedListProducts(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        ids_str = request.query_params.get('ids', '')  # Get the comma-separated string of IDs
        ids = [int(id_) for id_ in ids_str.split(',') if id_.strip().isdigit()]  # Parse IDs into integers
        
        if not ids:  # Handle case where no valid IDs are provided
            return Response({'status': 'Error', 'message': 'No valid IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"IDs: {ids}")
        
        # Fetch products based on the provided IDs
        products = Product.objects.filter(part_id__in=ids, status='Approved')
        print(f"Products: {products}")
        products_data = productinfoSerializer(products, many=True).data
        print(f"Products Data: {products_data}")
        
        return Response({'status': 'Success', 'data': products_data})
        
class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        user = request.user
        product = productinfo.objects.get(id=product_id, status='Approved')
        
        # Check if user has an active cart
        try:
            cart = Cart.objects.get(user=user, is_active=True)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        
        # Add product to the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)


class CartListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            # Retrieve only active cart items
            cart = Cart.objects.get(user=user, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Serialize each cart item individually
            cart_items_data = CartItemSerializer(cart_items, many=True).data
            return Response({'status': 'Success', 'data': cart_items_data})
        except Cart.DoesNotExist:
            return Response({'status': 'Error', 'data': 'Cart does not exist'})
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'status': 'Error', 'data': 'An error occurred'})

class UpdateQuantity(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        quantity = kwargs['quantity']
        user = request.user
        cart = Cart.objects.get(user=user.id, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, product=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({'message': 'Quantity updated successfully'}, status=status.HTTP_200_OK)
    
class RemoveFromCart(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        user = request.user
        cart = Cart.objects.get(user=user.id, is_active=True)
        cart_item = CartItem.objects.get(cart=cart, product=product_id)
        cart_item.delete()
        return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_200_OK)
    
class RemoveAllFromCart(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            cart = Cart.objects.get(user=user.id, is_active=True)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_items.delete()
            return Response({'message': 'All products removed from cart successfully'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({'message': 'No items in the cart to remove'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrderCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            cart_id = request.data.get('cart')
            cart = Cart.objects.get(id=cart_id)
            print("CART", cart)
            order = Order.objects.create(
                cart=cart,
                fullname=request.data.get('fullname'),
                phone=request.data.get('phone'),
                Address=request.data.get('Address'),
                payment_method=request.data.get('payment_method'),
                total_items=request.data.get('total_items'),
                total_price=request.data.get('total_price'),
            )
            # Mark the cart as inactive after the order is placed
            cart.is_active = False
            cart.save()
            
            return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetPartImage(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        try:
            partnumber = kwargs['partnumber']
            part = partNumber.objects.get(partNumber=partnumber)

            # Define the path to the directory
            dir_path = os.path.join(settings.MEDIA_ROOT, 'partimages', 'partimages', partnumber)

            # Check if the directory exists
            if not os.path.isdir(dir_path):
                return Response({'message': 'Part number does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Look for all image files in the directory
            matching_files = glob.glob(os.path.join(dir_path, '*'))

            # Convert the file paths to URLs
            # Convert the file paths to URLs
            matching_urls = [os.path.join(settings.MEDIA_URL, 'partimages', 'partimages', partnumber, os.path.basename(f)).replace('\\', '/') for f in matching_files]

            # Return the list of matching URLs
            return Response(matching_urls, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetAllOrders(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = request.user.id
        
        orders = Order.objects.filter(cart__user=user)
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_items_data = CartItemSerializer(cart_items, many=True).data
        orders_data = OrderSerializer(orders, many=True).data
        data = []
        
        for order in orders_data:
            cart_id = order['cart']
            cart_items = CartItem.objects.filter(cart__user=user,cart = cart_id)
            cart_items_data = CartItemSerializer(cart_items, many=True).data
            print("CART ITEMS", cart_items_data)
            order['cart_items'] = cart_items_data
            data.append(order)
        
        return Response({'status': 'Success', 'data': data})
    
    
class AddReturnReason(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)
        print("REQUEST DATA", request.data)
        return_reason = request.data.get('returnReason')
        print("RETURN REASON", return_reason)
        order.return_status = return_reason
        order.status = "Return Requested"
        order.save()
        return Response({'message': 'Return reason added successfully'}, status=status.HTTP_200_OK)