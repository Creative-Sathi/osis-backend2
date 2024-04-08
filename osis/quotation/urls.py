# urls.py
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ordercreate/', OrderCreateView.as_view(), name='order-create'),
    path('order-details/', IndivisualOrderDetailsView.as_view(), name='order-details'), 
    path('order-details/<int:order_id>/', OrderDetailsView.as_view(), name='order-details'),
    path('multiple-order-details/<int:order_id>/', MultipleQuotationView.as_view(), name='order-details'),
    
    
    path('creditdetails/', CreditDetailsView.as_view(), name='credit-details'),
   
    path('quotationcreate/<int:order_id>/<int:part_id>/<int:quantity>', QuotationCreateView.as_view(), name='quotation-create'),
    path('unidentified-products/', UnidentifiedProductCreateView.as_view(), name='unidentified-product-create'),
    path('seller-order-quotation-info/', SellerOrderQuotationInfoView.as_view(), name='seller-order-quotation-info'),
    path('seller-order-previous-quotation-info/', SellerOrderPreviousQuotationInfoView.as_view(), name='seller-order-previous-quotation-info'),
    path('filtered-quotations/', FilteredQuotationView.as_view(), name='filtered-quotations'),
    path('filtered-quotations/<str:status>/', FilteredQuotationStatusView.as_view(), name='filtered-quotations'),    
    path('createquotation/',SpecificSellerQuotationAdd.as_view(),name='createquotation'),
    path('updatestatus/',UpdateStatus.as_view(),name='updatestatus'),
    path('declinespecificquotation/',DeclineQuotationView.as_view(),name='declinespecificquotation'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
