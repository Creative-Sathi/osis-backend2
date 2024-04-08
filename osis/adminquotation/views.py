from rest_framework import generics, status
from rest_framework.response import Response
from quotation.models import *
from quotation.serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from profileseller.serializers import *
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from datetime import timedelta, datetime

class GetAllUnidentifiedProductsView(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        queryset = UnidentifiedProduct.objects.filter(status='Pending')
        serializer = ReadingUnidentifiedProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAllProcessingQuotationView(generics.ListAPIView):
    serializer_class = ReadingQuotationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        specificsellerQuotation = SpecificSellerQuotation.objects.filter(status='Pending')
        pending_quotations = Quotation.objects.filter(seller_quotation__in=specificsellerQuotation)
        return pending_quotations

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAllCancelledQuotationView(generics.ListAPIView):
    serializer_class = ReadingQuotationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        specificsellerQuotation = SpecificSellerQuotation.objects.filter(status='Declined')
        queryset = Quotation.objects.filter(seller_quotation__in=specificsellerQuotation)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAllCompletedOrderView(generics.ListAPIView):
    serializer_class = ReadingQuotationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        specificsellerQuotation = SpecificSellerQuotation.objects.filter(status='Completed')
        quotations = Quotation.objects.filter(seller_quotation__in=specificsellerQuotation).order_by('order_id')
        return quotations

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllProcessingOrderView(generics.ListAPIView):
    serializer_class = ReadingQuotationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        specificsellerQuotation = SpecificSellerQuotation.objects.filter(status='Accepted')
        quotations = Quotation.objects.filter(seller_quotation__in=specificsellerQuotation).order_by('order_id')
        return quotations

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
