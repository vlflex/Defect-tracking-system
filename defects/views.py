from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import DefectForm
from .models import ManufacturingDefect, Worker, Batch

@login_required
def defect_form(request):
    if request.method == 'POST':
        form = DefectForm(request.POST)
        if form.is_valid():
            try:
                defect = form.save(commit=False)
                defect.worker = form.cleaned_data['worker_tab_number']
                defect.save()
                messages.success(request, "Дефект успешно зарегистрирован")
                return redirect('defect_form')
            
            except Exception as e:
                messages.error(request, f"Ошибка при сохранении: {str(e)}")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = DefectForm()
    
    return render(request, 'defects/defect_form.html', {'form': form})

@login_required
def defect_list(request):
    defects = ManufacturingDefect.objects.all().select_related(
        'batch', 'workshop', 'worker', 'defect_type'
    ).order_by('-date')
    return render(request, 'defects/defect_list.html', {'defects': defects})