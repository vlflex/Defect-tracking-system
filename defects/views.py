from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import ManufacturingDefect, Worker, Equipment, Workshop, Batch, DefectType
from .forms import ManufacturingDefectForm

def home_view(request):
    """Главная страница сайта"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'total_defects': ManufacturingDefect.objects.count(),
        'total_equipment': Equipment.objects.count(),
        'total_users': 1
    }
    return render(request, 'home.html', context)

def defects_home_view(request):
    """Главная страница приложения дефектов"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'modules': [
            {
                'title': 'Ввод дефектов',
                'description': 'Быстрый и удобный ввод информации о дефектах производства',
                'url': '/defects/form/',
                'icon': '📝'
            },
            {
                'title': 'Список дефектов',
                'description': 'Просмотр и фильтрация всех зарегистрированных дефектов',
                'url': '/defects/list/',
                'icon': '📋'
            },
            {
                'title': 'Dashboard',
                'description': 'Аналитика и статистика по дефектам в реальном времени',
                'url': '/defects/dashboard/',
                'icon': '📈'
            }
        ]
    }
    return render(request, 'defects/home.html', context)

@login_required
def defect_form(request):
    if request.method == 'POST':
        form = ManufacturingDefectForm(request.POST)
        if form.is_valid():
            try:
                defect = form.save(commit=False)
                # Сохраняем табельный номер из выбранного работника
                worker = form.cleaned_data['worker_tab_num']
                defect.worker_tab_num = worker.tab_number
                defect.save()
                
                messages.success(request, f'Дефект успешно зарегистрирован! ID: {defect.id}')
                return redirect('defect_form')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ManufacturingDefectForm()
    
    # Получаем статистику для отображения
    total_defects = ManufacturingDefect.objects.count()
    recent_defects = ManufacturingDefect.objects.order_by('-date')[:5]
    
    return render(request, 'defects/defect_form.html', {
        'form': form,
        'total_defects': total_defects,
        'recent_defects': recent_defects
    })

@login_required
def defect_list(request):
    """Список всех дефектов"""
    # Получаем дефекты с предварительной загрузкой связанных данных
    defects = ManufacturingDefect.objects.select_related(
        'workshop', 'batch', 'equipment', 'defect_type'
    ).order_by('-date')
    
    # Фильтрация
    search_query = request.GET.get('search', '')
    workshop_id = request.GET.get('workshop', '')
    batch_id = request.GET.get('batch', '')
    
    if search_query:
        defects = defects.filter(
            Q(comment__icontains=search_query) |
            Q(worker_tab_num__icontains=search_query) |
            Q(batch__series__icontains=search_query)
        )
    
    if workshop_id:
        defects = defects.filter(workshop_id=workshop_id)
    
    if batch_id:
        defects = defects.filter(batch_id=batch_id)
    
    # Получаем данные для фильтров
    workshops = Workshop.objects.all()
    batches = Batch.objects.all().order_by('-start_date')[:20]
    
    return render(request, 'defects/defect_list.html', {
        'defects': defects,
        'workshops': workshops,
        'batches': batches,
        'search_query': search_query,
        'selected_workshop': workshop_id,
        'selected_batch': batch_id,
        'total_count': defects.count()
    })

@login_required
def dashboard_view(request):
    """Dashboard с аналитикой дефектов"""
    # Основные метрики
    total_defects = ManufacturingDefect.objects.count()
    
    # Дефекты за сегодня
    today = timezone.now().date()
    today_defects = ManufacturingDefect.objects.filter(
        date__date=today
    ).count()
    
    # Статистика по цехам
    workshop_stats = ManufacturingDefect.objects.values(
        'workshop__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Статистика по типам дефектов
    defect_type_stats = ManufacturingDefect.objects.values(
        'defect_type__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Статистика по оборудованию
    equipment_stats = ManufacturingDefect.objects.filter(
        equipment__isnull=False
    ).values(
        'equipment__name',
        'workshop__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Динамика за 7 дней
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_stats = []
    
    # Собираем данные по дням
    for i in range(7):
        date = timezone.now() - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        count = ManufacturingDefect.objects.filter(
            date__range=(date_start, date_end)
        ).count()
        
        daily_stats.append({
            'date': date,
            'count': count,
            'trend': 0  # Для простоты оставляем 0
        })
    
    # Реверсируем список для отображения от старых к новым
    daily_stats.reverse()
    
    # Количество цехов с дефектами
    workshop_count = ManufacturingDefect.objects.values(
        'workshop'
    ).distinct().count()
    
    # Количество оборудования
    equipment_count = Equipment.objects.count()
    
    context = {
        'total_defects': total_defects,
        'today_defects': today_defects,
        'workshop_stats': workshop_stats,
        'defect_type_stats': defect_type_stats,
        'equipment_stats': equipment_stats,
        'daily_stats': daily_stats,
        'workshop_count': workshop_count,
        'equipment_count': equipment_count,
    }
    
    return render(request, 'defects/dashboard.html', context)

@login_required
def defect_detail(request, defect_id):
    """Детальная информация о дефекте"""
    defect = get_object_or_404(
        ManufacturingDefect.objects.select_related(
            'workshop', 'batch', 'equipment', 'defect_type'
        ),
        id=defect_id
    )
    
    # Получаем информацию о работнике
    worker_info = None
    if defect.worker_tab_num:
        try:
            worker = Worker.objects.get(tab_number=defect.worker_tab_num)
            worker_info = {
                'name': f"{worker.last_name} {worker.first_name}",
                'position': worker.get_position_display(),
                'tab_number': worker.tab_number
            }
        except Worker.DoesNotExist:
            worker_info = {'error': 'Работник не найден'}
    
    return render(request, 'defects/defect_detail.html', {
        'defect': defect,
        'worker_info': worker_info
    })