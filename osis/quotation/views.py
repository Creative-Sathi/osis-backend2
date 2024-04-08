# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from profileseller.serializers import *
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from admindashboard.models import Credit
from django.db.models import Sum


class OrderCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # Manually set requested_seller_id to 2
        data = request.data
        user_id = request.user.id
        seller = Seller.objects.get(seller=user_id)
        data['requested_seller_id'] = seller.id

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
# views.py
class QuotationCreateView(generics.CreateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        selected_products = request.data
        order_id = kwargs.get('order_id')  # Get order_id from the URL
        part_id = kwargs.get('part_id')  # Get part_id from the URL
        quantity = kwargs.get('quantity')  # Get quantity from the URL
        stat = "Pending"
        
        
        quotation_data = {
            'order_id': order_id,
            'part_id': part_id, # Set this to the product_info later
            'quantity': quantity,
            'status': stat,
            'seller_quotation': None  # Set this to the seller_quotation later
        }

        quotation_serializer = self.get_serializer(data=quotation_data)
        quotation_serializer.is_valid(raise_exception=True)
        quotation_serializer.save()
        print(quotation_serializer.data)

        return Response({"message": "Quotations created successfully"}, status=status.HTTP_201_CREATED)

class UnidentifiedProductCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    
    # Create Unidentified Product from the data passed in the request
    def create(self, request, *args, **kwargs):
        data = request.data
        serializers = UnidentifiedProductSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SellerOrderQuotationInfoView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self,current_seller_id): # Assuming the user is a Seller
        orders = Order.objects.filter(requested_seller_id=current_seller_id)
        order_ids = orders.values_list('id', flat=True)
        filted_orders_id = Order.objects.filter(id__in=order_ids)
        filtered_orders_time = filted_orders_id.filter(dateandtime__gte=timezone.now()-timedelta(minutes=10))
        
        return filtered_orders_time
    
    

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        current_seller_id = Seller.objects.get(seller=user_id).id
        print("Current Seller ID: ", current_seller_id)
        queryset = self.get_queryset(current_seller_id)
        serializer = self.serializer_class(queryset, many=True)

        data = []
        for order in queryset:
            products_count = Quotation.objects.filter(order_id=order.id).count()

            # Count products from UnidentifiedProduct model
            unidentified_products_count = UnidentifiedProduct.objects.filter(order_id=order.id).count()

            # Total count including both identified and unidentified products
            total_products_count = products_count + unidentified_products_count

            data.append({
                'order_no': order.id,
                'products_count': total_products_count
            })

        return Response(data)

class SellerOrderPreviousQuotationInfoView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


    def get_queryset(self,current_seller_id):# Assuming the user is a Seller
        orders = Order.objects.filter(requested_seller_id=current_seller_id)
        order_ids = orders.values_list('id', flat=True)
        filted_orders_id = Order.objects.filter(id__in=order_ids)
        filtered_orders_time = filted_orders_id.filter(dateandtime__lte=timezone.now()-timedelta(minutes=10)) 
        return filtered_orders_time
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        current_seller_id = Seller.objects.get(seller=user_id).id
        queryset = self.get_queryset(current_seller_id)
        serializer = self.serializer_class(queryset, many=True)

        data = []
        for order in queryset:
            products = Quotation.objects.filter(order_id=order.id)
            products_count = products.count()
            unidentified_products = UnidentifiedProduct.objects.filter(order_id=order.id)
            unidentified_products_count = unidentified_products.count()
            status_list = []
            for product in products:
                specificseller = product.seller_quotation
                if specificseller is None:
                    statusspecific = "Cancelled"
                else:
                    statusspecific = specificseller.status
                status_list.append(statusspecific)
            for product in unidentified_products:
                status_list.append(product.status)
            
            if all(status == "Accepted" for status in status_list):
                order_status = "Processing"
            elif all(status == "Completed" for status in status_list):
                order_status = "Completed"
            elif all(status == "Cancelled" for status in status_list):
                order_status = "Cancelled"
            elif any(status == "Pending" or status == "Rejected" for status in status_list):
                order_status = "Rejected"
            
            total_products_count = products_count + unidentified_products_count
            data.append({
                'order_no': order.id,
                'date_and_time': order.dateandtime.strftime('%Y-%m-%d %H:%M'), # Format: 'YYYY-MM-DD HH:MM
                'products_count': total_products_count,
                'order_status': order_status
            })

        return Response(data)

class IndivisualOrderDetailsView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        current_seller_id = request.seller.id  # Assuming the user is a Seller
        orders = Order.objects.filter(requested_seller_id=current_seller_id)
        order_ids = orders.values_list('id', flat=True)
        filtered_orders = Order.objects.filter(id__in=order_ids)
        return filtered_orders

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        data = []
        for order in queryset:
            # Count products from Quotation model with 'Completed' status
            completed_products_count = Quotation.objects.filter(order_id=order.id, status='Completed').count()

            # Count total products from Quotation model
            total_products_count = Quotation.objects.filter(order_id=order.id).count()

            # Check if all products have 'Completed' status
            order_status = 'Completed' if completed_products_count == total_products_count else 'Pending'

            data.append({
                'order_no': order.id,
                'date_and_time': order.dateandtime.strftime('%Y-%m-%d %H:%M'),
                'products_count': total_products_count,
                'status': order_status
            })

        return Response(data)

class FilteredQuotationView(APIView):
    serializer_class = ReadingQuotationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,current_seller_id):
        pending_quotations = Quotation.objects.filter(status='Pending')
        products_list = productinfo.objects.filter(seller_id=current_seller_id).values_list('part_id', flat=True)
        
        pending_quotations = pending_quotations.filter(part_id__in=products_list)
        print(pending_quotations)
        same_order_ids = Order.objects.filter(requested_seller_id=current_seller_id).values_list('id', flat=True)
        print(same_order_ids)
        filtered_orders_time = Order.objects.filter(dateandtime__lte=timezone.now()-timedelta(minutes=10)).values_list('id', flat=True)
        invalid_order_ids = list(same_order_ids) + list(filtered_orders_time)
        filtered_quotations_order_time = pending_quotations.exclude(order_id__in=invalid_order_ids)
        print(filtered_quotations_order_time)
        return filtered_quotations_order_time

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        current_seller_id = Seller.objects.get(seller=user_id).id
        queryset = self.get_queryset(current_seller_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FilteredQuotationStatusView(APIView):
    serializer_class = ReadingSpecificSellerQuotationSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self, requested_status, current_seller_id):
        filtered_status_quotations = SpecificSellerQuotation.objects.filter(status=requested_status , quoted_seller_id=current_seller_id)
        specific_seller_quotation_ids = Quotation.objects.all().values_list('seller_quotation', flat=True)
        filtered_specific_seller_quotations = filtered_status_quotations.filter(id__in=specific_seller_quotation_ids)
        
        return filtered_specific_seller_quotations
    

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        current_seller_id = Seller.objects.get(seller=user_id).id
        requested_status = kwargs.get('status')
        queryset = self.get_queryset(requested_status=requested_status, current_seller_id=current_seller_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  
class OrderDetailsView(APIView):
    serializer_class = ReadingQuotationSerializer
    permission_classes = [AllowAny]
    
    # Get all the details of Table Quotation if order_id matches with the order id of passed parameter
    def get(self,args, **kwargs):
        order_id = kwargs.get('order_id')
        queryset = Quotation.objects.filter(order_id=order_id)
        serializer_data = self.serializer_class(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)   
    
class MultipleQuotationView(APIView):
    serializer_class = ReadingSpecificSellerQuotationSerializer
    permission_classes = [AllowAny,]
    
    def get(self,request, **kwargs):
        order_id = kwargs.get('order_id')
        queryset = SpecificSellerQuotation.objects.filter(quotation_id__order_id=order_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# View to add in SpecificSellerQuotation table
class SpecificSellerQuotationAdd(APIView):
    serializer_class = SpecificSellerQuotationSerializer
    permission_classes = [IsAuthenticated,]
    
    def post(self,request, **kwargs):
        data = request.data
        print(data)
        quotation_id = data['quotation_id']
        user_id = request.user.id
        current_seller_id = Seller.objects.get(seller=user_id).id# Assuming the user is a Seller
        stat = "Pending"
        quoted_price_per_unit = data['perUnitPrice']
        # Convert the total price to integer
        quoted_total_price = float(data['total'])
        delivery_period = data['deliveryTime']
        remarks = data['remarks']
        all_specific_seller_of_quotation = SpecificSellerQuotation.objects.filter(quotation_id=quotation_id)
        for quoation in all_specific_seller_of_quotation:
            if quoation.quoted_seller_id == current_seller_id:
                quotation.update(quoted_price_per_unit=quoted_price_per_unit, quoted_price_total=quoted_total_price, delivery_period=delivery_period, remarks=remarks) 
                return Response({"message": "SpecificSellerQuotation updated successfully"}, status=status.HTTP_201_CREATED)
        else:
            data = {
            'quotation_id': quotation_id,
            'quoted_seller_id': current_seller_id,
            'status': stat,
            'quoted_price_per_unit': quoted_price_per_unit,
            'quoted_price_total': quoted_total_price,
            'delivery_period': delivery_period,
            'remarks': remarks
        }
        
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   
# Update Status in Model SpecificSellerQuotation
class UpdateStatus(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request, **kwargs):
        data = request.data
        print(data)
        specific_seller_quotation_id = data['specific_seller_quotation_id']
        stat = data['status']
        
        if stat == "Accepted":
            SpecificSellerQuotation_data = SpecificSellerQuotation.objects.get(id=specific_seller_quotation_id)
            Quotation_object = Quotation.objects.get(id=SpecificSellerQuotation_data.quotation_id.id)
            
            order_id = Quotation_object.order_id
            Order_data = Order.objects.get(id=order_id.id)
            requestedseller_id = Order_data.requested_seller_id
            
            credit_data = Credit.objects.get(seller_profile=requestedseller_id)
            
            balance = credit_data.balance
            amount_to_pay = SpecificSellerQuotation_data.quoted_price_total
            
            if balance < amount_to_pay:
                return Response({"message": "Insufficient Balance"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                credit_data.balance = credit_data.balance - amount_to_pay
                Order_data.remaining_balance = credit_data.balance
                credit_data.balance_updated = datetime.now()
                if credit_data.credit_provided != 0:
                    credit_data.credit_used = datetime.now()
                
                
                credit_data.save()
                Order_data.save()
                
            Quotation_object.status = stat
            Quotation_object.seller_quotation = SpecificSellerQuotation_data
            Quotation_object.save()
            
            SpecificSellerQuotation_data.status = stat            
            SpecificSellerQuotation_data.save()
            
            return Response({"message": "Status updated successfully"}, status=status.HTTP_201_CREATED)
                

        
        
        try:
            with transaction.atomic():
                # Get the SpecificSellerQuotation instance
                specific_seller_quotation_instance = SpecificSellerQuotation.objects.get(id=specific_seller_quotation_id)
                specific_seller_quotation_instance.status = stat
                specific_seller_quotation_instance.save()
                
                return Response({"message": "Status updated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": "Status not updated"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeclineQuotationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request, **kwargs):
        data = request.data
        specific_seller_quotation_id = data['specific_seller_quotation_id']
        
        try:
            with transaction.atomic():
                # Get the SpecificSellerQuotation instance
                specific_seller_quotation_instance = SpecificSellerQuotation.objects.get(id=specific_seller_quotation_id)
                specific_seller_quotation_instance.status = "Declined"
                specific_seller_quotation_instance.remarks = data['remarks']
                specific_seller_quotation_instance.save()
                
                return Response({"message": "SpecificSellerQuotation updated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"message": "Status not updated"}, status=status.HTTP_400_BAD_REQUEST)
        
        

class CreditDetailsView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, current_seller_id):
        orders = Order.objects.filter(requested_seller_id=current_seller_id)
        order_ids = orders.values_list('id', flat=True)
        filtered_orders = Order.objects.filter(id__in=order_ids)
        return filtered_orders

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        current_seller_id = Seller.objects.get(seller=user_id).id
        
        queryset = self.get_queryset(current_seller_id)
        serializer = self.serializer_class(queryset, many=True)

        data = []
        for order in queryset:
            quotation_data = Quotation.objects.filter(order_id=order.id)
            seller_quotation = quotation_data.values_list('seller_quotation', flat=True)
            transaction_data = SpecificSellerQuotation.objects.filter(id__in=seller_quotation)
            total_quoted_price = transaction_data.aggregate(total=Sum('quoted_price_total'))['total'] or 0.0
            print(transaction_data)
            data.append({
                'order_id': order.id,
                'order_date': order.dateandtime.strftime('%Y-%m-%d %H:%M'),
                'order_value': total_quoted_price,
                'remaining_balance': order.remaining_balance
            })

        return Response(data)

