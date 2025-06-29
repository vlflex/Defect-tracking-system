from django import forms
from django.utils import timezone
from .models import ManufacturingDefect, Worker, Batch

class DefectForm(forms.ModelForm):
    worker_tab_number = forms.CharField(
        label="Табельный номер рабочего",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите 3-значный номер (например: 101)'
        })
    )
    
    class Meta:
        model = ManufacturingDefect
        fields = ['batch', 'defect_type', 'workshop', 'comment']
        labels = {
            'batch': 'Партия',
            'defect_type': 'Тип дефекта',
            'workshop': 'Производственный цех',
            'comment': 'Комментарий'
        }
        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'workshop': forms.Select(attrs={'class': 'form-control'}),
            'defect_type': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только активные партии для выпадающего списка
        active_batches = Batch.objects.filter(
            finish_date__isnull=True
        ) | Batch.objects.filter(
            finish_date__gte=timezone.now()
        )
        self.fields['batch'].queryset = active_batches
        
    def clean_worker_tab_number(self):
        tab_number = self.cleaned_data['worker_tab_number']
        try:
            return Worker.objects.get(tab_number=tab_number)
        except Worker.DoesNotExist:
            raise forms.ValidationError('Работник с таким табельным номером не найден')
    
    def clean(self):
        cleaned_data = super().clean()
        workshop = cleaned_data.get('workshop')
        batch = cleaned_data.get('batch')
        
        if workshop and batch:
            supported_series = workshop.get_supported_series()
            # Если цех - отдел качества (id=3), пропускаем проверку
            if workshop.id != 3 and batch.series not in supported_series:
                self.add_error('workshop', "Неправильно выбранная партия или цех")
                self.add_error('batch', "Неправильно выбранная партия или цех")
        
        return cleaned_data