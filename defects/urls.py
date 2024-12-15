from django.urls import path
from . import views

urlpatterns = [
    path('', views.defects_home_view, name='defects_home'),
    path('form/', views.defect_form, name='defect_form'),
    path('list/', views.defect_list, name='defect_list'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('<int:defect_id>/', views.defect_detail, name='defect_detail'),
]