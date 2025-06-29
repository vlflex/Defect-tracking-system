from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
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
    
    position = models.IntegerField(choices=POSITION_CHOICES, null=True, blank=True)
    tab_number = models.CharField(max_length=10, unique=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )

class Workshop(models.Model):
    name = models.CharField(max_length=100)
    series_array = models.JSONField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'workshops'
        

class DefectType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'defect_types'

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

    def __str__(self):
        return f"Партия {self.id} ({self.series})"

class ManufacturingDefect(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, verbose_name="Партия")
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, verbose_name="Цех")
    worker = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Рабочий")
    defect_type = models.ForeignKey(DefectType, on_delete=models.CASCADE, verbose_name="Тип дефекта")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"Дефект {self.id} (партия {self.batch_id})"

    class Meta:
        verbose_name = "Дефект производства"
        verbose_name_plural = "Дефекты производства"
        db_table = 'manufacturing_defects'