from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('input_department/', views.EntryDepartmentView.as_view(), name='input_department'),
    path('input_bulk_users/', views.InputBulkUsersView.as_view(), name='input_bulk_users'),
]
