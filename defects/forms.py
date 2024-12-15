from django import forms
from .models import ManufacturingDefect, Batch, Workshop, DefectType, Worker, Equipment
from django.db.models import Q

class ManufacturingDefectForm(forms.ModelForm):
    worker_tab_num = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        label="Работник",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.all(),
        label="Партия",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    defect_type = forms.ModelChoiceField(
        queryset=DefectType.objects.all(),
        label="Тип дефекта",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    workshop = forms.ModelChoiceField(
        queryset=Workshop.objects.all(),
        label="Производственный цех",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label="Оборудование",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    comment = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Дополнительная информация о дефекте...'
        }),
        required=False
    )
    
    class Meta:
        model = ManufacturingDefect
        fields = ['worker_tab_num', 'batch', 'defect_type', 'workshop', 'equipment', 'comment']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка queryset для поля работника
        self.fields['worker_tab_num'].queryset = Worker.objects.all().order_by('last_name', 'first_name')
        self.fields['worker_tab_num'].label_from_instance = lambda obj: f"{obj.tab_number} - {obj.last_name} {obj.first_name}"
        
        # Настройка queryset для партий (только активные)
        self.fields['batch'].queryset = Batch.objects.filter(
            finish_date__isnull=True
        ).order_by('-start_date')[:50]
        
        # Настройка queryset для оборудования (только активное)
        self.fields['equipment'].queryset = Equipment.objects.filter(
            status='active'
        ).order_by('name')