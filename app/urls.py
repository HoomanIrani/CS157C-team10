from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('professor_dashboard/', views.faculty_dashboard, name='professor_dashboard'),
	path('coordinator_dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
]