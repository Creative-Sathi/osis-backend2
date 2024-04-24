from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('search/<str:search>',SearchedProducts.as_view()),
    path('search/product/',SearchedListProducts.as_view()),
    path('searchedproduct/<int:id>',SpecificSearchedProducts.as_view()),
    path('similarproducts/<int:id>',SimilarProducts.as_view()),
    path('add_to_cart/<int:product_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('buy-now/<int:product_id>/', BuyNow.as_view(), name='buy_now'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('update_quantity/<int:product_id>/<int:quantity>/', UpdateQuantity.as_view(), name='update_quantity'),
    path('remove_from_cart/<int:product_id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('remove_all_from_cart/', RemoveAllFromCart.as_view(), name='remove_all_from_cart'),
    path('update_cart_items/', UpdateCartItemsStatus.as_view(), name='update_cart_items'),
    
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
    
    path('getpartimage/<str:partnumber>',GetPartImage.as_view()),
    
    
    path('getallorders/', GetAllOrders.as_view()),
    
    path('addreturnreason/<int:order_id>',AddReturnReason.as_view()),
    
    path('create-review/', create_review.as_view(), name='create_review'),
    path('getmyreviews/', GetMyReviews.as_view()),
    
    path('productreview/<int:product_id>', ProductReview.as_view()),
    
    
    path('address/', UserAddressOperation.as_view(), name='address'),
    path('address/<int:address_id>/', UserAddressOperation.as_view(), name='address-detail'),
    
    path('getaddresses/', GetAddresses.as_view()),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)