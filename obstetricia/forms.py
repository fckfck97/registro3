from django import forms
from .models import Paciente_obstetricia,Parto,Nota,Orden_medica_parto,Antecedentes,Examen_fisico
from datetime import datetime
from django.utils import timezone, dateformat
from django.shortcuts import get_object_or_404


class Paciente_obstetriciaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Paciente_obstetriciaForm, self).__init__(*args, **kwargs)
		self.fields['fecha'].required = False
		self.fields['cedula'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Cedula de Identidad',
                                        'tabindex':'1'
                                    })
		self.fields['nombre'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nombres',
                                        'tabindex':'2'
                                    })
		self.fields['apellido'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Apellidos',
                                        'tabindex':'3'
                                    })
	
		self.fields['edad'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Edad',
                                        'tabindex':'4'
                                    })
		self.fields['direccion'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Direccion',
                                        'tabindex':'5'
                                    })
		self.fields['telefono'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'04241234567',
                                        'tabindex':'6'
                                    })

	class Meta:
		model = Paciente_obstetricia
		fields =[
            'cedula',
            'nombre',
            'apellido',
            'edad',
            'direccion',
            'fecha',
            'telefono',
        ]


class PartoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PartoForm, self).__init__(*args, **kwargs)
		self.fields['ci_paciente'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Cedula de Identidad',
                                        'tabindex':'1'
                                    })
		self.fields['motivo_consulta'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Motivo',
                                        'tabindex':'2'
                                    })
		self.fields['presenta'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Enfermedad Actual',
                                        'tabindex':'3'
                                    })
		self.fields['diagnostico'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Diagnostico',
                                        'tabindex':'4'
                                    })
		self.fields['controles'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Controles',
                                        'min':'0', 
                                        'pattern':'^[0-9]+',
                                        'tabindex':'27'
                                    })
		self.fields['deseado'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        
                                        'tabindex':'28'
                                    })
		self.fields['planificado'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        
                                        'tabindex':'29'
                                    })
		self.fields['controlado'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        
                                        'tabindex':'30'
                                    })
		self.fields['itu'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        
                                        'tabindex':'31'
                                    })
		self.fields['laboratorio'].widget = forms.Textarea(attrs={
                                        'class':'form-control',
                                        'placeholder':'Laboratorio',
                                        'tabindex':'32'
                                    })
	
	class Meta:
		model = Parto
		fields =[
            'ci_paciente',
            'motivo_consulta',
            'presenta',
            'diagnostico',
            'controles',
            'deseado',
            'planificado',
            'controlado',
            'itu',
            'laboratorio',
        ]

class AntecedentesForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AntecedentesForm, self).__init__(*args, **kwargs)
		self.fields['gestas'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Gestas',
                                        'min':'0', 
                                        'pattern':'^[0-9]+',
                                        'tabindex':'5'
                                    })
		self.fields['partos'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Partos',
                                        'min':'0',
                                        'pattern':'^[0-9]+',
                                        'tabindex':'6'
                                    })
		self.fields['cesareas'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Cesareas',
                                        'min':'0',
                                        'pattern':'^[0-9]+',
                                        'tabindex':'7'
                                    })
		self.fields['legrados'].widget =forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Legrados',
                                        'pattern':'^[0-9]+',
                                        'tabindex':'8'
                                    })
		self.fields['fur'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
										'placeholder':'01/01/2020',
                                        'tabindex':'9'
                                    })
		self.fields['antemadre'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de la Madre',
                                        'tabindex':'10'
                                    })
		self.fields['antepadre'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes del Padre',
                                        'tabindex':'11'
                                    })
		self.fields['antehermanos'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de los Hermanos',
                                        'tabindex':'12'
                                    })
		self.fields['antehijos'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de los Hijos',
                                        'tabindex':'13'
                                    })
		self.fields['patologias'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de Patologia Base',
                                        'tabindex':'14'
                                    })
		self.fields['alergias'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de Alergias',
                                        'tabindex':'15'
                                    })
		self.fields['transfusiones'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de Transfuciones',
                                        'tabindex':'16'
                                    })
		self.fields['intervenciones'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Antecedentes de Intervensiones QX',
                                        'tabindex':'17'
                                    })
		self.fields['menarquia'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Menarquia',
                                        'min':'10', 
                                        'pattern':'^[0-9]+',
                                        'tabindex':'18'
                                    })
		self.fields['sexarquia'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Sexarquia',
                                        'min':'10', 
                                        'pattern':'^[0-9]+',
                                        'tabindex':'19'
                                    })
		self.fields['ciclomens'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Ciclos Menstruales',
                                   
                                        'tabindex':'20'
                                    })
		self.fields['parejas'].widget = forms.NumberInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Numero de Parejas',
                                        'min':'0',
                                        'max':'10',
                                        'pattern':'^[0-9]+',
                                        'tabindex':'21'
                                    })
		self.fields['aco'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        'tabindex':'22'
                                    })
		self.fields['citologia'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        'tabindex':'23'
                                    })
		self.fields['its'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        'tabindex':'24'
                                    })
		self.fields['diu'].widget = forms.NullBooleanSelect(attrs={
                                        'class':'form-control',
                                        'tabindex':'25'
                                    })
		self.fields['embarazo_ante'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Embarazo Anterior',
                                        'tabindex':'26'
                                    })






	class Meta:
		model = Antecedentes
		fields =[
            'gestas',
            'partos',
            'cesareas',
            'legrados',
            'fur',
            'antemadre',
            'antepadre',
            'antehermanos',
            'antehijos',
            'patologias',
            'alergias',
            'transfusiones',
            'intervenciones',
            'menarquia',
            'sexarquia',
            'ciclomens',
            'parejas',
            'aco',
            'citologia',
            'its',
            'diu',
            'embarazo_ante',
        ]		

	

class NotaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(NotaForm, self).__init__(*args, **kwargs)
		self.fields['nota_seis'].required = False
		self.fields['nota_siete'].required = False
		self.fields['nota_ocho'].required = False
		self.fields['nota_nueve'].required = False
		self.fields['nota_diez'].required = False
        

		self.fields['ci_paciente'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Cedula de Identidad',
                                        'tabindex':'1'
                                    })
		self.fields['nota_uno'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Uno',
                                        'tabindex':'2'
										
                                    })
		self.fields['nota_dos'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Dos',
                                        'tabindex':'3'
										
                                    })
		self.fields['nota_tres'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Tres',
                                        'tabindex':'4'
										
                                    })
		self.fields['nota_cuatro'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Cuatro',
                                        'tabindex':'5'
										
                                    })
		self.fields['nota_cinco'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Cinco',
                                        'tabindex':'6'
										
                                    })
		self.fields['nota_seis'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Seis',
                                        'tabindex':'7'
										
                                    })
		self.fields['nota_siete'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Siete',
                                        'tabindex':'8'
										
                                    })
		self.fields['nota_ocho'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Ocho',
                                        'tabindex':'9'
										
                                    })
		self.fields['nota_nueve'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Nueve',
                                        'tabindex':'10'
										
                                    })
		self.fields['nota_diez'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Nota Diez',
                                        'tabindex':'11'
										
                                    })
		self.fields['diagnostico2'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Diagnostico',
                                        'tabindex':'12'
										
                                    })

	class Meta:
		model = Nota
		fields =[
            'ci_paciente',
            'nota_uno',
            'nota_dos',
            'nota_tres',
            'nota_cuatro',
            'nota_cinco',
            'nota_seis',
            'nota_siete',
            'nota_ocho',
            'nota_nueve',
            'nota_diez',
            'diagnostico2',
        
        ]		

class OrdenForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(OrdenForm, self).__init__(*args, **kwargs)
		self.fields['orden_ocho'].required = False
		self.fields['orden_nueve'].required = False
		self.fields['orden_diez'].required = False

		self.fields['ci_paciente'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Cedula de Identidad',
                                        'tabindex':'1'
                                    })
		self.fields['orden_uno'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Uno',
                                        'tabindex':'2'
										
                                    })
		self.fields['orden_dos'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Dos',
                                        'tabindex':'3'
										
                                    })
		self.fields['orden_tres'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Tres',
                                        'tabindex':'4'
										
                                    })
		self.fields['orden_cuatro'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Cuatro',
                                        'tabindex':'5'
										
                                    })
		self.fields['orden_cinco'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Cinco',
                                        'tabindex':'6'
										
                                    })
		self.fields['orden_seis'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Seis',
                                        'tabindex':'7'
										
                                    })
		self.fields['orden_siete'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Siete',
                                        'tabindex':'8'
										
                                    })
		self.fields['orden_ocho'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Ocho',
                                        'tabindex':'9'
										
                                    })
		self.fields['orden_nueve'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Nueve',
                                        'tabindex':'10'
										
                                    })
		self.fields['orden_diez'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Orden Diez',
                                        'tabindex':'11'
										
                                    })

	class Meta:
		model = Orden_medica_parto
		fields =[
            'ci_paciente',
            'orden_uno',
            'orden_dos',
            'orden_tres',
            'orden_cuatro',
            'orden_cinco',
            'orden_seis',
            'orden_siete',
            'orden_ocho',
            'orden_nueve',
            'orden_diez',
        
        ]

class Examen_fisicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Examen_fisicoForm, self).__init__(*args, **kwargs)
        
        self.fields['feto'].required = False

        self.fields['ci_paciente'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Cedula de Identidad',
                                        'tabindex':'1'
                                    })
        self.fields['ta'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Tension Arterial',
                                        'tabindex':'2'
                                        
                                    })
        self.fields['fc'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Frecuencia Cardiaca',
                                        'tabindex':'3'
                                        
                                    })
        self.fields['fr'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Frecuencia Respiratoria',
                                        'tabindex':'4'
                                        
                                    })
        self.fields['cardio_pul'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'CardioPulmonar',
                                        'tabindex':'5'
                                        
                                    })
        self.fields['mamas'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Mamas',
                                        'tabindex':'6'
                                        
                                    })
        self.fields['abdomen'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Abdomen',
                                        'tabindex':'7'
                                        
                                    })
        self.fields['feto'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Feto',
                                        'tabindex':'8'
                                        
                                    })
        self.fields['normoconfigurados'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Vagina',
                                        'tabindex':'9'
                                        
                                    })
        self.fields['cuello_uterino'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Cuello Uterino',
                                        'tabindex':'10'
                                        
                                    })
        self.fields['extremidades'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Extremidades',
                                        'tabindex':'11'
                                        
                                    })
        self.fields['neurologico'].widget = forms.TextInput(attrs={
                                        'class':'form-control',
                                        'placeholder':'Neurologico',
                                        'tabindex':'12'
                                        
                                    })

    class Meta:
        model = Examen_fisico
        fields =[
            'ci_paciente',
            'ta',
            'fc',
            'fr',
            'cardio_pul',
            'mamas',
            'abdomen',
            'feto',
            'normoconfigurados',
            'cuello_uterino',
            'extremidades',
            'neurologico',
        
        ]		



	