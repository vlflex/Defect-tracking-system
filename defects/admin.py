from django.contrib import admin
from .models import Worker, Workshop, DefectType, Batch, ManufacturingDefect

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('tab_number', 'first_name', 'last_name', 'get_position_display')
    list_display_links = ('tab_number',)
    search_fields = ('tab_number', 'first_name', 'last_name')
    ordering = ('tab_number',)

admin.site.register(Workshop)
admin.site.register(DefectType)
admin.site.register(Batch)
admin.site.register(ManufacturingDefect)