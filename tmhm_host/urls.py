"""OnlineLearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('LandingPage.api.urls')),
     path('', include('myauth.urls')),
    path('', include('facilitators.api.urls')),
    path('', include('myauth.api.urls')),
    path('', include('payment_gateway.urls')),
    path('', include('corporates.urls')),
    path('', include('LandingPage.urls')),
    path('', include('facilitators.urls')),
    path('', include('learners.urls')),
    path('', include('campus.urls')),
    path('', include('mailing.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
