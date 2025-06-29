from django.contrib import admin
from .models import User, Workshop, DefectType, Batch, ManufacturingDefect

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_position_display', 'tab_number')

admin.site.register(Workshop)
admin.site.register(DefectType)
admin.site.register(Batch)
admin.site.register(ManufacturingDefect)