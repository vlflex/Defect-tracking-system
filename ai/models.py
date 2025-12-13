from django.db import models
from defects.models import EquipmentModel, Batch, Equipment

# AI-компоненты
class AIAgent(models.Model):
    name = models.CharField(max_length=100)
    equipment_model = models.ForeignKey(
        EquipmentModel, on_delete=models.PROTECT)
    accuracy = models.FloatField()
    status_choices = [
        ('active', 'Активен'),
        ('training', 'Обучение'),
        ('inactive', 'Неактивен')
    ]
    status = models.CharField(max_length=20, choices=status_choices)

    class Meta:
        db_table = 'ai_agents'

    def __str__(self):
        return f"{self.name} ({self.status})"


class AIRecommendation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    batch = models.ForeignKey(
        Batch, on_delete=models.CASCADE, null=True, blank=True)
    decision_choices = [
        ('continue', 'Продолжить эксплуатацию'),
        ('retire', 'Списать оборудование')
    ]
    decision = models.CharField(max_length=20, choices=decision_choices)
    justification = models.TextField()

    class Meta:
        db_table = 'ai_recommendations'

    def __str__(self):
        return f"Рекомендация {self.id} ({self.decision})"
