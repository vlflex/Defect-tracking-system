from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from defects.views import home_view, defects_home_view
from ai.views import ai_home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='defects/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('defects/', include('defects.urls')),
    path('ai/', include('ai.urls')),
]