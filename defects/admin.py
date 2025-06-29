from django.contrib import admin
from .models import Worker, Workshop, DefectType, Batch, ManufacturingDefect
from django.utils.html import format_html

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('tab_number', 'first_name', 'last_name', 'get_position_display')
    list_display_links = ('tab_number',)
    search_fields = ('tab_number', 'first_name', 'last_name')
    ordering = ('tab_number',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'series', 'formatted_start_date', 'formatted_finish_date', 'status')
    list_display_links = ('id', 'series')
    search_fields = ('series',)
    ordering = ('-start_date',)
    
    def formatted_start_date(self, obj):
        return obj.start_date.strftime('%d.%m.%Y %H:%M')
    formatted_start_date.short_description = 'Дата начала'
    
    def formatted_finish_date(self, obj):
        if obj.finish_date is None:
            return "Производится"
        return obj.finish_date.strftime('%d.%m.%Y %H:%M')
    formatted_finish_date.short_description = 'Дата окончания'
    
    def status(self, obj):
        if obj.is_active():
            return format_html('<span style="color: green;">Активна</span>')
        return format_html('<span style="color: red;">Завершена</span>')
    status.short_description = 'Статус'

admin.site.register(Workshop)
admin.site.register(DefectType)
admin.site.register(ManufacturingDefect)