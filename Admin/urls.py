from django.urls import path
from . import views

urlpatterns = [
    path('learnopad/admin/manage/learners', views.manage_learners, name='manage_learners'),
    path('learnopad/admin/edit/learners/', views.view_edit_learners, name='view_edit_learners'),
    path('learnopad/admin/dashboard/', views.Dashboard, name='dashboard_admin'),
    path('learnopad/admin/manage/Courses/', views.manage_courses, name='manage_courses'),
    path('learnopad/admin/manage/facilitators/', views.manage_facilitators, name='manage_facilitators'),
    path('learnopad/admin/edit/facilitators/', views.view_edit_facilitators, name='view_edit_facilitators'),
    path('learnopad/admin/edit/Courses/', views.view_edit_courses, name='view_edit_courses'),
    path('learnopad/admin/Approved/Courses/', views.Approved_courses, name='Approved_courses'),
    path('learnopad/admin/Approved/facilitators/', views.Approved_facilitators, name='Approved_facilitators'),
    path('learnopad/admin/view/campus/', views.campus_training, name='campus_training'),
    path('learnopad/admin/view/corporate/', views.cor_training, name='cor_training'),
    path('learnopad/admin/view/queries/', views.query_submission, name='query_submission'),
    





]
