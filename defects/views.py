from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import DefectForm
from .models import ManufacturingDefect, User

@login_required
def defect_form(request):
    if request.method == 'POST':
        form = DefectForm(request.POST)
        if form.is_valid():
            try:
                worker = User.objects.get(tab_number=form.cleaned_data['worker_tab_number'])
                defect = form.save(commit=False)
                defect.worker = worker
                defect.date = timezone.now()
                defect.save()
                return redirect('defect_form')
            except User.DoesNotExist:
                form.add_error('worker_tab_number', 'Работник с таким табельным номером не найден')
    else:
        form = DefectForm()
    
    return render(request, 'defects/defect_form.html', {'form': form})

@login_required
def defect_list(request):
    defects = ManufacturingDefect.objects.all().order_by('-date')
    return render(request, 'defects/defect_list.html', {'defects': defects})