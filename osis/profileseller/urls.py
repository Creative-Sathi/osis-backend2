from django.contrib import admin
from django.urls import path
from django.conf import settings
from profileseller.views import *
from django.conf.urls.static import static
urlpatterns = [
    path('sellerprofile/', SellerProfileView.as_view(),name='sellerprofile'),
    path('address/', AddressView.as_view(),name='address'),
    path('selleraddress/', SellerAddressView.as_view(),name='selleraddress'),
    path('documents/', DocumentsView.as_view(),name='documents'),
    path('seller/',SellerView.as_view(),name='seller'),
    path('updateprofileseller/',UpdateProfileSellerView.as_view(),name='updateprofileseller'),
    path('updateaddressseller/',UpdateAddressView.as_view(),name='updateaddress'),
    path('getsellerprofile/',GetSellerProfileView.as_view(),name='getsellerprofile'),
    path('getallrequestedseller/',GetallrequestedSeller.as_view(),name='getallrequestedseller'),
    path('getallapprovedseller/',GetAllApprovedSeller.as_view(),name='getallapprovedseller'),
    path('getallrejectedseller/',GetAllRejectedSeller.as_view(),name='getallrejectedseller'),
    path('managevendor/',ManageVendor.as_view(),name='managevendor'),
    path('profile/',GetAllSpecificSellerDetails.as_view(),name='profiledetails'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)