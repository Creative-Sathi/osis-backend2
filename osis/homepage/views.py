from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
from sellerdashboard.models import *
from django.db.models import Count
from django.db.models.functions import Coalesce
from rest_framework import status
from sellerdashboard.models import productinfo

class FeaturedProjectView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            featuredproduct = FeaturedProduct.objects.all()
            
            featuredproduct = featuredproduct.reverse()
            featuredproduct = featuredproduct[:10]
            serializer = FeaturedProductSerializer(featuredproduct, many=True)            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        try:
            serializer = FeaturedProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryCountAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        categories_with_counts = (
            partinfo.objects
            .values('partCategories')
            .filter(status='Approved')
            .annotate(product_count=Coalesce(Count('Part'), 0))
            .filter(product_count__gt=0) 
            .distinct()
        )
        
        print(categories_with_counts)
        serializer = CategoryCountSerializer(categories_with_counts, many=True)
        return Response(serializer.data)
    
class TopCarMakerAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        topcarmaker = (
            partinfo.objects
            .values('brand')
            .filter(status='Approved')
            .annotate(product_count=Coalesce(Count('Part'), 0))
            .filter(product_count__gt=0) 
            .distinct()
        )
        serializer = TopCarMakerSerializer(topcarmaker, many=True)
        return Response(serializer.data)
    

class LatestProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        try:
            latestproduct = productinfo.objects.filter(status='Approved')
            latestproduct = latestproduct.reverse()
            latestproduct = latestproduct[:10]
            serializer = LatestProductSerializer(latestproduct, many=True)            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)