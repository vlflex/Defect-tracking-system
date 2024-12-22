from django.urls import path
from .views import ai_home_view, model_info_view, api_predict, model_info, check_equip

urlpatterns = [
    path('', ai_home_view, name='ai_home'),
    path('model-info/', model_info_view, name='model_info'),
    path('check-equip/', check_equip, name='check_equip'),
    path('check-equip/<int:equipment_id>/', check_equip, name='check_equip_by_id'),
    path('api/predict/<int:equipment_id>/', api_predict, name='api_predict'),
    path('api/model-info/', model_info, name='api_model_info'),
]