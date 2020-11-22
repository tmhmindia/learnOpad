from .views import *
from django.urls import path


urlpatterns = [
    path('user/signup/', signup, name='signup'),
    path('user/login/', user_login.as_view(), name="login"),
    path('user/signin/', login_page, name="login_page"),
    path('user/logout/', user_logout, name="logout"),
    path('changepassword/', ChangePassword, name="changePassword"),
    path('recoverpassword/<int:pk>/', forgot_password, name="forgotPassword"),
]
 