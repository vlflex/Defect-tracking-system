from django import forms
from .models import ManufacturingDefect, DefectType, Workshop, User

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
        fields = ['defect_type', 'workshop', 'comment']
        labels = {
            'defect_type': 'Тип дефекта',
            'workshop': 'Производственный цех',
            'comment': 'Комментарий'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({'class': 'form-control'})
            elif field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 3
                })