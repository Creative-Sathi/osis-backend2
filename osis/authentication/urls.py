from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from authentication.views import *
# from django.conf.urls.static import static
# from django.conf import settings

# +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [

    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('sendotp/',UserOtpView.as_view(),name='send-otp'),
    path('changepassword/',UserChangePasswordView.as_view(),name='changepassword'),
    path('updatepassword/',UserUpdatePasswordView.as_view(),name='updatepassword'),
    
    path('getallusers/',GetAllUsersView.as_view(),name='getallusers'),
    path('updaterole/<int:id>/<str:role>/',UpdateRoleView.as_view(),name='updaterole'),
    path('getallagents/',GetAllAgentsView.as_view(),name='getallusers'),
    path('getbannedusers/',GetBannedUsersView.as_view(),name='getbannedusers'),
    
    path('getuserdetails/<str:username>/',GetUserDetailsView.as_view(),name='getuserdetails'),
    path('updateuser/<int:id>/',UpdateUserView.as_view(),name='updateuser'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
