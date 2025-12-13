from django.contrib import admin
from .models import AIAgent, AIRecommendation

admin.site.register(
    [
        AIAgent,
        AIRecommendation,
    ]
    
)
