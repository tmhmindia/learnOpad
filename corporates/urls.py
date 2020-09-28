from django.urls import path
from . import views

urlpatterns = [
    path('corporates/', views.corporate_landingPage, name='corporates'),
]
