from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Справочные сущности
class Worker(models.Model):
    POSITION_CHOICES = [
        ('ОПЛ', 'Оператор производственной линии'),
        ('ТП', 'Технолог производства'),
        ('МЦ', 'Мастер цеха'),
        ('ИПК', 'Инженер по качеству'),
        ('КОТК', 'Контролер ОТК'),
        ('НС', 'Начальник смены'),
        ('ТЭ', 'Техник-электроник'),
        ('СР', 'Сборщик реле'),
        ('АИС', 'Администратор информационной системы'),
    ]
    tab_number = models.CharField(max_length=20, primary_key=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, null=True, blank=True)  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'workers'
        managed = False

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.tab_number})"
    
    def get_position_display(self):
        """Получить отображаемое название должности"""
        return dict(self.POSITION_CHOICES).get(self.position, "Не указана")


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


# Оборудование
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
    status = models.CharField(max_length=20, choices=status_choices, default='active')

    class Meta:
        db_table = 'equipment'

    def __str__(self):
        return self.name

    @property
    def age_months(self):
        return (timezone.now().date() - self.start_date).days // 30


class EquipmentProduction(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField()
    units_produced = models.IntegerField()

    class Meta:
        db_table = 'equipment_production'
        unique_together = ('equipment', 'date')
        verbose_name = 'Производство оборудования'
        verbose_name_plural = 'Производство оборудования'

    def __str__(self):
        return f"{self.equipment.name} - {self.date}: {self.units_produced} ед."


class ManufacturingDefect(models.Model):
    worker_tab_num = models.CharField(max_length=50, verbose_name="Табельный номер работника")
    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT, verbose_name="Цех")
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, verbose_name="Оборудование")
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, verbose_name="Партия")
    defect_type = models.ForeignKey(DefectType, on_delete=models.PROTECT, verbose_name="Тип дефекта")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    
    # Свойство для получения объекта Worker по табельному номеру
    @property
    def worker(self):
        try:
            return Worker.objects.get(tab_number=self.worker_tab_num)
        except Worker.DoesNotExist:
            return None
    
    class Meta:
        db_table = 'manufacturing_defects'
        verbose_name = 'Дефект производства'
        verbose_name_plural = 'Дефекты производства'
        ordering = ['-date']
    
    def __str__(self):
        return f"Дефект #{self.id} от {self.date.strftime('%d.%m.%Y')}"


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