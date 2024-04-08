from django.urls import path
from .views import *

urlpatterns = [
    path('get-all-unidentified-products/', GetAllUnidentifiedProductsView.as_view(), name='get-all-unidentified-products'),
    path('get-all-processing-quotation/', GetAllProcessingQuotationView.as_view(), name='get-all-processing-quotation'),
    path('get-all-cancelled-quotation/', GetAllCancelledQuotationView.as_view(), name='get-all-cancelled-quotation'),
    path('get-all-completed-order/', GetAllCompletedOrderView.as_view(), name='get-all-completed-order'),
    path('get-all-processing-order/', GetAllProcessingOrderView.as_view(), name='get-all-processing-order'),
    
]