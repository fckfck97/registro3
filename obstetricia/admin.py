from django.contrib import admin
from .models import Paciente_obstetricia,Parto,Nota,Medico_obs,Antecedentes
# Register your models here.
class NotaAdmin(admin.ModelAdmin):
    list_display = ('ci_paciente', 'nota_uno', 'nota_dos', 'nota_tres', 'nota_cuatro', 'nota_cinco', 'nota_seis', 'nota_siete', 'nota_ocho', 'diagnostico2')
    
class Paciente_obstetriciaAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'edad', 'direccion', 'fecha')

class PartoAdmin(admin.ModelAdmin):
    list_display = ('ci_paciente', 'motivo_consulta', 'presenta', 'diagnostico')

class Medico_obsAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','genero')

admin.site.register(Paciente_obstetricia,Paciente_obstetriciaAdmin)
admin.site.register(Parto,PartoAdmin)
admin.site.register(Nota,NotaAdmin)
admin.site.register(Medico_obs,Medico_obsAdmin)
admin.site.register(Antecedentes)