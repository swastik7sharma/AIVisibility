"""
URL configuration for tracker app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Project workflow
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/validate/', views.validate_project, name='validate_project'),
    path('project/<int:project_id>/models/', views.select_models, name='select_models'),
    path('project/<int:project_id>/execute/', views.execute_check, name='execute_check'),
    path('project/<int:project_id>/status/', views.check_status, name='check_status'),
    path('project/<int:project_id>/report/', views.view_report, name='view_report'),
    
    # Competitor impersonation
    path('project/<int:project_id>/impersonate/<int:competitor_id>/', 
         views.competitor_impersonation, 
         name='competitor_impersonation'),
    
    # API
    path('api/project/<int:project_id>/status/', views.api_project_status, name='api_project_status'),
]
