from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from sellerdashboard.views import *
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'addproduct',ProductinfoView)

urlpatterns = [
    path('addproduct/',ProductinfoView.as_view()),
    path('editproduct/',EditProductInfoView.as_view()),
    # path('updateproductdetails/',UpdateProductDetailsView.as_view()),
    path('allproduct/',ApprovedProductSpecificInfoView.as_view()),
    path('deletedproduct/',DeletedProductInfoView.as_view()),
    path('updateproduct/',UpdateProductInfoView.as_view()),
    path('searchproduct/',ApprovedProductInfoView.as_view()),
    path('agentsearchproduct/',AgentApprovedProductInfoView.as_view()),
    
    path('removeproduct/',RemoveProductInfoView.as_view()),
    path('redoproduct/',RedoProductInfoView.as_view()),
    
    path('reviewproduct/',ReviewProductInfoView.as_view()),
    path('adminreviewproduct/',AdminReviewProductInfoView.as_view()),
    
    path('acceptreviewproduct/',AcceptReviewProductInfoView.as_view()),
    
    path('addproductcsv/', UploadProductInfoView.as_view()),
    
    path('order/<str:currentstatus>/',OrderInfoView.as_view()),
    path('adminorder/<str:currentstatus>/',AdminOrderInfoView.as_view()),
    path('changeorderstatus/<str:order_id>/<str:newstatus>/',ChangeOrderStatusView.as_view()),
    
    path('balancedetails/',BalanceDetailsView.as_view()),
    
    path('getmyreviews/',GetMyReviews.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
