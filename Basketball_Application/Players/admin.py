
from django.contrib import admin
from .models import Player,Scouting_Context,Report_Model

class PlayerModelAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Player._meta.fields]
class Scouting_Context_Admin(admin.ModelAdmin):
    list_display=[field.name for field in Scouting_Context._meta.fields]

class ReportModelAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Report_Model._meta.fields]


admin.site.register(Player,PlayerModelAdmin)
admin.site.register(Scouting_Context,Scouting_Context_Admin)
admin.site.register(Report_Model,ReportModelAdmin)
