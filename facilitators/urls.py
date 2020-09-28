from django.urls import path
from . import views

urlpatterns = [
    path('facilitator/dashboard/explore', views.facilitator_Dashboard_explore_courses_page, name="explorecourses"),
    path('facilitator/dashboard/earnings', views.facilitator_Dashboard_myearnings_page, name="earnings"),
    # path('facilitator/recoverpassword/<int:pk>/', views.forgot_password, name="forgotPassword"),
    path('facilitator/dashboard/create_course', views.facilitator_Dashboard_create_course_page, name="createcourse"),
    path('facilitator/dashboard/', views.facilitator_Dashboard_Landing_page,name="dashboard"),
    path('facilitator/', views.facilitator_page,name='facilitator'),
    #path('facilitator-register/', views.RegisterLoginView.as_view(),name='facilitator-register'),
    path('facilitator/dashboard/settings/', views.facilitator_Dashboard_settings_page,name='settings'),
    path('facilitator/dashboard/profile/', views.facilitator_Profile_page,name='profile'),
    path('facilitator/dashboard/support/', views.facilitator_Dashboard_support_page,name='support'),
    # path('facilitator/dashboard/changepassword/', views.ChangePassword, name="changePassword"),
    path('facilitator/dashboard/support/', views.facilitator_Dashboard_support_page,name='support1'),
    path('About/facilitator/<int:pk>/',views.aboutfacilitator, name="aboutfacilitator"),
 ]
     