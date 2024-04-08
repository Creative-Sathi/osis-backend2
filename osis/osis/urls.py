"""
URL configuration for osis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include("authentication.urls")),
    path('api/newseller/',include("profileseller.urls")),
    path('api/sellerdashboard/',include("sellerdashboard.urls")),    
    path('api/admin/',include("admindashboard.urls")),
    path('api/quotation/',include("quotation.urls")),
    path('api/admin/quotation/',include("adminquotation.urls")),
    path('api/homepage/',include("homepage.urls")),
    path('api/users/',include("users.urls")),
    
    # path('api/chat/',include("chat.urls")),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
