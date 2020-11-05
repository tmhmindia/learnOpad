from django.urls import path
from . import views

urlpatterns = [
    path('learnopad/admin/manage/learners', views.manage_learners, name='manage_learners'),
    path('learnopad/admin/edit/learners/', views.view_edit_learners, name='view_edit_learners'),
    path('learnopad/admin/dashboard/', views.Dashboard, name='dashboard_admin'),


]
