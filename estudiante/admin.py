from django.contrib import admin
from models import Taller,Curso,Academic_Rank,Seguimiento,Estado,TallerGeneral
# Register your models here.

class Academic_RankAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha','hora','actividad','nota','nivel','firma_alumno','profesor',)
    list_editable = ('actividad','nota','nivel','firma_alumno','profesor',)
    search_fields = ('estudiante__cedula',)
    ordering = ('-fecha',)
    raw_id_fields = ('estudiante',)

class TallerAdmin(admin.ModelAdmin):
	list_display = ('tema','fecha','hora_inicio','hora_fin','capacidad','profesor','lugar','nivel',)
	filter_horizontal = ('estudiantes',)

class TallerGAdmin(admin.ModelAdmin):
    list_display = ('tema','fecha','hora_inicio','hora_fin','capacidad','profesor','lugar',)
    filter_horizontal = ('alumnos',)

class CursoAdmin(admin.ModelAdmin):
	list_display = ('fecha','hora_inicio','hora_fin','capacidad_maxima','sede','profesor','tipo_nivel','tipo_leccion','max_tipo',)
	list_editable = ('profesor',)
	list_filter = ('sede','hora_inicio',)
	filter_horizontal = ('estudiantes','tipo_estudiante',)


class SeguimientoAdmin(admin.ModelAdmin):
	list_display = ('estudiante','comentario','estado',)
	list_filter = ('estado',)
	list_editable = ('estado',)
	raw_id_fields = ('estudiante',)


admin.site.register(Taller,TallerAdmin)
admin.site.register(TallerGeneral,TallerGAdmin)
admin.site.register(Curso,CursoAdmin)
admin.site.register(Academic_Rank,Academic_RankAdmin)
admin.site.register(Seguimiento,SeguimientoAdmin)
admin.site.register(Estado)