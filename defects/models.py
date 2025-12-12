from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


# Основные справочные сущности
class Worker(models.Model):
    POSITION_CHOICES = [
        (1, 'Оператор производственной линии'),
        (2, 'Технолог'),
        (3, 'Мастер цеха'),
        (4, 'Инженер по качеству'),
        (5, 'Контролер ОТК'),
        (6, 'Начальник смены'),
        (7, 'Техник-электроник'),
        (8, 'Сборщик реле'),
        (9, 'Администратор системы'),
    ]
    tab_number = models.CharField(max_length=10, primary_key=True)
    position = models.IntegerField(
        choices=POSITION_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'workers'
        managed = False

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.tab_number})"


class Workshop(models.Model):
    name = models.CharField(max_length=100)
    series_array = models.JSONField()

    class Meta:
        db_table = 'workshops'

    def __str__(self):
        return self.name

    def get_supported_series(self):
        return self.series_array if isinstance(self.series_array, list) else []


class DefectType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'defect_types'

    def __str__(self):
        return self.name


class Batch(models.Model):
    SERIES_CHOICES = [
        ('РЭС52', 'РЭС52'),
        ('РЭС64А ОС', 'РЭС64А ОС'),
        ('РЭС78 ОС', 'РЭС78 ОС'),
        ('РЭК107', 'РЭК107'),
        ('РЭК 90', 'РЭК 90'),
        ('РГК37', 'РГК37'),
        ('РГК 37 Б-В', 'РГК 37 Б-В'),
        ('РЭН34', 'РЭН34'),
        ('РЭН 34-Т ОС', 'РЭН 34-Т ОС'),
    ]
    series = models.CharField(max_length=20, choices=SERIES_CHOICES)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'batches'
        verbose_name_plural = 'Партии'

    def __str__(self):
        return f"Партия {self.id} ({self.series})"

    def is_active(self):
        if self.finish_date is None:
            return True
        return timezone.now().date() <= self.finish_date.date()


# Основные процессные сущности
class EquipmentModel(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    supported_series = models.JSONField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    lifetime_months = models.IntegerField()

    class Meta:
        db_table = 'equipment_models'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    model = models.ForeignKey(EquipmentModel, on_delete=models.PROTECT)
    start_date = models.DateField()
    status_choices = [
        ('active', 'Активно'),
        ('maintenance', 'На обслуживании'),
        ('retired', 'Списано')
    ]
    status = models.CharField(
        max_length=20, choices=status_choices, default='active')

    class Meta:
        db_table = 'equipment'

    def __str__(self):
        return self.name


class ManufacturingDefect(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    defect_type = models.ForeignKey(DefectType, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'manufacturing_defects'
        verbose_name = "Дефект производства"
        verbose_name_plural = "Дефекты производства"

    def __str__(self):
        return f"Дефект {self.id} (партия {self.batch_id})"

    def clean(self):
        if self.batch and self.workshop:
            supported_series = self.workshop.get_supported_series()
            if self.workshop.id != 3 and self.batch.series not in supported_series:
                raise ValidationError("Неправильно выбранная партия или цех")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField()
    maintenance_type = models.CharField(max_length=100)
    duration_hours = models.FloatField()
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'maintenance'

    def __str__(self):
        return f"Обслуживание {self.id} ({self.equipment.name})"


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
