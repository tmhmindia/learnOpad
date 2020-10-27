from django.urls import path, re_path
from .views import *


app_name = 'chat'

urlpatterns = [
    
    path('experts/<str:group_id>/',room, name='room')
]
