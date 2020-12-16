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
    path('learnopad/admin/Delete/Course/', views.DeleteCourse, name='delete_course'),
    path('learnopad/admin/Delete/User/', views.DeleteUser, name='delete_user'),
    path('learnopad/admin/Delete/contact/Councelling/', views.DeleteCouncellingContactUsData, name='delete_contactus_councelling'),
    path('learnopad/admin/Delete/Training/', views.DeleteTrainingData, name='delete_training'),
    path('learnopad/admin/learner/support/', views.learner_support, name='admin_to_learner_support'),
    path('learnopad/admin/facilitator/support/', views.facilitator_support, name='facilitator_support'),
    path('learnopad/admin/course/orders/', views.course_orders, name='course_orders'),
    path('learnopad/admin/facilitator/orders/', views.facilitator_orders, name='facilitator_orders'),
    path('learnopad/admin/myprofile/', views.myprofile, name='myprofile'), 
    path('learnopad/admin/category/', views.category, name='categorymanage'),
    path('learnopad/admin/subcategory/', views.subcategory, name='subcategory'),   
    path('learnopad/admin/Delete/query/', views.DeleteSupportQueires, name='Delete_support_queries'),
    path('learnopad/admin/Delete/Subscription/', views.DeleteSubscription, name='delete_subscription'),
    path('learnopad/admin/Delete/Order/Course', views.DeleteOrderCourse, name='delete_order_course'),
    path('learnopad/admin/staff/', views.staff, name='staff'),
    path('learnopad/admin/Delete/Category/', views.DeleteCategorySubcategory, name='delete_CatSubcat'),
   






]
