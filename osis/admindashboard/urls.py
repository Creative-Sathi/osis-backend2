from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from admindashboard.views import *
urlpatterns = [
    path('addpart/',PartinfoView.as_view()),
    path('addpartcsv/', UploadPartInfoView.as_view()),
    path('approved-partinfo/',ApprovedPartInfoView.as_view()),
    path('csv-partinfo/',CSVPartInfoView.as_view()),
    path('seller-partinfo/',SellerAddedPartInfoView.as_view()),
    path('deleted-partinfo/',DeletedPartInfoView.as_view()),
    path('update-partinfo/',UpdatePartInfoView.as_view()),
    path('undo-partinfo/',UndoPartInfoView.as_view()),
    path('delete-partinfo/',DeletePartInfoView.as_view()),
    path('update-part/<int:pk>/',PartinfoAPIView.as_view()),
    
    path('get-company/',CompanyInfoView),
    path('brandinfo/<str:company>/', BrandInfoView, name='brand_info'),
    path('modelinfo/<str:company>/<str:brand>/', ModelInfoView, name='model_info'),
    path('get-partcategories/',PartCategoryView),
    
    path('allapprovedproduct/',ApprovedProductInfoView.as_view()),
    path('makefeaturedproduct/<int:id>/',MakeFeaturedProduct.as_view()),
    path('listfeaturedproduct/',ListFeaturedProduct.as_view()),
    path('removefeaturedproduct/<int:id>/',RemoveFeaturedProduct.as_view()),
    
    path('get-credit/',AllCreditView.as_view()),
    path('update-credit/',UpdateCreditView.as_view()),
    
    path('uploadpartimages/',upload_folder),
    path('getpartimages/<str:folder_name>/',partimageview.as_view()),
    
    path('companyimages/',CompanyImagesView.as_view()),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
