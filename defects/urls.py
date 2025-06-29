from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.defect_form, name='defect_form'),
    path('list/', views.defect_list, name='defect_list'),
    path('login/', auth_views.LoginView.as_view(template_name='defects/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]