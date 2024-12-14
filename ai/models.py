from django.db import models
from defects.models import Equipment, Batch

class AIAgent(models.Model):
    """Упрощенная модель AI агента"""
    name = models.CharField(max_length=100, verbose_name="Название")
    version = models.CharField(max_length=20, default="1.0", verbose_name="Версия")
    accuracy = models.FloatField(default=0.0, verbose_name="Точность")
    status_choices = [
        ('active', 'Активен'),
        ('training', 'Обучение'),
        ('inactive', 'Неактивен')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='active', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    model_path = models.CharField(max_length=255, blank=True, verbose_name="Путь к модели")
    
    class Meta:
        db_table = 'ai_agents'
        verbose_name = 'AI агент'
        verbose_name_plural = 'AI агенты'
    
    def __str__(self):
        return f"{self.name} v{self.version} ({self.status})"

class AIRecommendation(models.Model):
    """Рекомендация от AI"""
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE, verbose_name="Агент")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Оборудование")
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Партия")
    
    decision_choices = [
        ('continue', 'Продолжить эксплуатацию'),
        ('repair', 'Требуется ремонт'),
        ('retire', 'Списать оборудование'),
        ('monitor', 'Усилить мониторинг')
    ]
    decision = models.CharField(max_length=20, choices=decision_choices, verbose_name="Решение")
    probability = models.FloatField(default=0.0, verbose_name="Вероятность")
    justification = models.TextField(verbose_name="Обоснование")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")
    confirmed_by = models.CharField(max_length=100, blank=True, verbose_name="Подтвердил")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата подтверждения")
    
    class Meta:
        db_table = 'ai_recommendations'
        verbose_name = 'AI рекомендация'
        verbose_name_plural = 'AI рекомендации'
        ordering = ['-date_created']
    
    def __str__(self):
        return f"Рекомендация #{self.id} для {self.equipment.name}: {self.get_decision_display()}"