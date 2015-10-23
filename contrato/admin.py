from django.contrib import admin
from models import Contrato,Ciudad,Sede,Estudiante,Programa,Nivel,Profesor


class SedeAdmin(admin.ModelAdmin):
		list_display = ('nombre_sede','ciudad','direccion','telefono','hora_inicio','hora_fin')

class NivelAdmin(admin.ModelAdmin):
		list_display = ('nivel','leccion')

class EstudianteAdmin(admin.ModelAdmin):
		list_display = ('usuario','cedula','nombre','apellido','telefono','programa','sede','nivel','fecha_de_inicio','fecha_de_expiracion')
		list_filter = ('sede','nivel')
		list_editable = ('nivel',)
		search_fields = ('cedula',)
		raw_id_fields = ('usuario',)
        
class ContratoAdmin(admin.ModelAdmin):
		list_display = ('numero_contrato','numero_factura','nombre','apellidos','cedula','email','telefono','celular','fecha_creacion','duracion','sede_firma_contrato')
		list_filter = ('sede_firma_contrato',)
		search_fields = ('numero_contrato',)
		filter_horizontal = ('beneficiarios',)

class ProfesorAdmin(admin.ModelAdmin):
  list_display = ('cedula','nombre','apellido','sede')
  list_filter = ('sede',)
  search_fields = ('nombre',)


admin.site.register(Contrato,ContratoAdmin)
admin.site.register(Ciudad)
admin.site.register(Sede,SedeAdmin)
admin.site.register(Estudiante,EstudianteAdmin)
admin.site.register(Programa)
admin.site.register(Nivel,NivelAdmin)
admin.site.register(Profesor,ProfesorAdmin)



