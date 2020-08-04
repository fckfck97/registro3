from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone, dateformat
from django.template.loader import render_to_string
from .forms import Paciente_obstetriciaForm,PartoForm,NotaForm,OrdenForm,AntecedentesForm,Examen_fisicoForm
from .models import Paciente_obstetricia,Parto,Nota,Orden_medica_parto,Antecedentes,Examen_fisico
#decorador de login para porder ver las vistas si se esta logeado en el sistema
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#libreria para la generacion del pdf
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.colors import pink
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import TemplateView, CreateView, DetailView



class Inicio(LoginRequiredMixin, TemplateView):
    template_name = 'obstetricia/inicio.html'

class Buscar(LoginRequiredMixin,TemplateView):
    template_name = 'obstetricia/buscar_obs.html'

class Paciente_Create(LoginRequiredMixin, CreateView):
    template_name = 'obstetricia/index_obs.html'    
    model = Paciente_obstetricia
    form_class = Paciente_obstetriciaForm
    def post(self, request, *args, **kwargs):
        success = []
        errors = []
        form = self.form_class()
        form_data = request.POST or None
        form_post = self.form_class(form_data)
        if request.method == 'POST':
            if 'cedula' in request.POST:
                ci_paciente = request.POST['cedula']
                persona = Paciente_obstetricia.objects.filter(cedula=ci_paciente).exists()
                if persona ==  True:
                    errors.append("Ya existe un Paciente Registrado con ese Numero de Cedula %s"%ci_paciente)
                else:
                    self.form_valid(form_post)
                    success.append('Se han Guardado los Datos Correctamente')
            
            return render(request, self.template_name, {'form': form,'success':success,'errors':errors})
    
    def form_valid(self, form):
        formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
        self.object = form.save(commit=False)
        self.object.fecha = formatted_date
        return super(Paciente_Create, self).form_valid(form)

class Examen_Fisico_Create(LoginRequiredMixin, CreateView):
    template_name = 'obstetricia/examen_fisico.html'    
    model = Examen_fisico
    form_class = Examen_fisicoForm
    def post(self, request, *args, **kwargs):
        success = []
        errors = []
        form = self.form_class()
        form_data = request.POST or None
        form_post = self.form_class(form_data)
        if request.method == 'POST':
            if 'ci_paciente' in request.POST:
                ci_paciente = request.POST['ci_paciente']
                persona = Paciente_obstetricia.objects.filter(cedula=ci_paciente).exists()
                if persona ==  True:
                    cedula_id = Paciente_obstetricia.objects.get(cedula=ci_paciente)
                    request.POST._mutable = True
                    request.POST['ci_paciente'] = cedula_id.id
                    request.POST._mutable = False
                    self.form_valid(form_post)
                    success.append('Se han Guardado los Datos Correctamente')
                else:
                    errors.append("Paciente C.I:%s. No esta registrada procede a registrarla"%ci_paciente)
                    form = self.form_class()
            
            return render(request, self.template_name, {'form': form,'success':success,'errors':errors})

    def form_valid(self, form):
        formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
        self.object = form.save(commit=False)
        self.object.fecha = formatted_date
        self.object.medico_nombre = self.request.user.first_name
        self.object.medico_apellido = self.request.user.last_name
        self.object.genero = self.request.user.genero
        self.object.rango = self.request.user.rango
        return super(Examen_Fisico_Create, self).form_valid(form)

class Nota_Parto_Create(LoginRequiredMixin ,CreateView):
    template_name = 'obstetricia/parto/nota_parto.html'    
    model = Nota
    form_class = NotaForm
    def post(self, request, *args, **kwargs):
        success = []
        errors = []
        form = self.form_class()
        form_data = request.POST or None
        form_post = self.form_class(form_data)
        if request.method == 'POST':
            if 'ci_paciente' in request.POST:
                ci_paciente = request.POST['ci_paciente']
                persona = Paciente_obstetricia.objects.filter(cedula=ci_paciente).exists()
                if persona ==  True:
                    cedula_id = Paciente_obstetricia.objects.get(cedula=ci_paciente)
                    request.POST._mutable = True
                    request.POST['ci_paciente'] = cedula_id.id
                    request.POST._mutable = False
                    self.form_valid(form_post)
                    success.append('Se han Guardado los Datos Correctamente')
                else:
                    errors.append("Paciente C.I:%s. No esta registrada procede a registrarla"%ci_paciente)
                    form = self.form_class()
            return render(request, self.template_name, {'form': form,'success':success,'errors':errors})

    def form_valid(self, form):
        formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
        self.object = form.save(commit=False)
        self.object.fecha = formatted_date
        self.object.medico_nombre = self.request.user.first_name
        self.object.medico_apellido = self.request.user.last_name
        self.object.genero = self.request.user.genero
        self.object.rango = self.request.user.rango
        return super(Nota_Parto_Create, self).form_valid(form)
    
class Orden_Medica_Parto_Create(LoginRequiredMixin, CreateView):
    template_name = 'obstetricia/parto/orden_medica_parto.html'    
    model = Orden_medica_parto
    form_class = OrdenForm
    def post(self, request, *args, **kwargs):
        success = []
        errors = []
        form = self.form_class()
        form_data = request.POST or None
        form_post = self.form_class(form_data)
        if request.method == 'POST':
            if 'ci_paciente' in request.POST:
                ci_paciente = request.POST['ci_paciente']
                persona = Paciente_obstetricia.objects.filter(cedula=ci_paciente).exists()
                if persona ==  True:
                    cedula_id = Paciente_obstetricia.objects.get(cedula=ci_paciente)
                    request.POST._mutable = True
                    request.POST['ci_paciente'] = cedula_id.id
                    request.POST._mutable = False
                    self.form_valid(form_post)
                    success.append('Se han Guardado los Datos Correctamente')
                else:
                    errors.append("Paciente C.I:%s. No esta registrada procede a registrarla"%ci_paciente)
                    form = self.form_class()
            return render(request, self.template_name, {'form': form,'success':success,'errors':errors})

    def form_valid(self, form):
        formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
        self.object = form.save(commit=False)
        self.object.fecha = formatted_date
        self.object.medico_nombre = self.request.user.first_name
        self.object.medico_apellido = self.request.user.last_name
        self.object.genero = self.request.user.genero
        self.object.rango = self.request.user.rango
        
        return super(Orden_Medica_Parto_Create, self).form_valid(form)

        
class Parto_Create(LoginRequiredMixin, TemplateView):
    template_name = 'obstetricia/parto/parto_registro.html'
    def dispatch(self, request, *args, **kwargs):
        self.form = PartoForm(request.POST or None)
        self.form2 = AntecedentesForm(request.POST or None)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        return {'form': self.form, 'form2': self.form2}

    def form_valid(self, form, form2):
        formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
        self.object = form.save(commit=False)
        self.object2 = form2.save(commit=False)
        self.object.fecha = formatted_date
        return super(Parto_Create, self).form_valid(form,form2)
    


class Buscar_Paciente(DetailView):
    template_name = "obstetricia/resultado.html"
    model = Paciente_obstetricia, Parto
    def post(self, request, *args, **kwargs):
        buscar = "obstetricia/buscar_obs.html"
        try:
            errors = []
            if 'cedula' in request.POST:
                cedula = request.POST['cedula']
                persona = Paciente_obstetricia.objects.filter(cedula=cedula).exists()
                if not cedula:
                    errors.append('Por favor introduce un Numero de Cedula.')
                elif len(cedula) > 9 or len(cedula) < 7:
                    errors.append('Por favor introduce un Numero de Cedula de entre 8 caracteres y 9 caracteres.')
                elif persona == False:
                    errors.append("No existe un Paciente con el numero de cedula %s proceda a registrarlo."%cedula)
                else:
                    paciente = Paciente_obstetricia.objects.filter(cedula=cedula)
                    for p in paciente:
                        parto = Parto.objects.all().filter(ci_paciente_id=p.id)
            return render(request, self.template_name, {'paciente': paciente,'parto':parto}) 
        except:
            return render(request,buscar, {'errors': errors})
        

        
@login_required
def buscar_paciente(request):   
    errors = []
    if 'cedula' in request.POST:
        cedula = request.POST['cedula']
        persona = Paciente_obstetricia.objects.filter(cedula=cedula).exists()
        if not cedula:
            errors.append('Por favor introduce un Numero de Cedula.')
        elif len(cedula) > 9 or len(cedula) < 7:
            errors.append('Por favor introduce un Numero de Cedula de entre 8 caracteres y 9 caracteres.')
        elif persona == False:
            errors.append("No existe un Paciente con el numero de cedula %s proceda a registrarlo."%cedula)
        else:
            paciente = Paciente_obstetricia.objects.filter(cedula=cedula)
            for p in paciente:
                parto = Parto.objects.all().filter(ci_paciente_id=p.id)
            
            return render(request, 'obstetricia/resultado.html',{'paciente': paciente,'parto': parto})
                
                
    return render(request, 'obstetricia/buscar_obs.html', {'errors': errors})

#vista del modal crear paciente
@login_required
def paciente_create(request):
    formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
    data = dict()
    if request.method == 'POST':
        form = Paciente_obstetriciaForm(request.POST)
        if form.is_valid():
            exito = form.save(commit=False)
            exito.fecha = formatted_date
            exito.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = Paciente_obstetriciaForm()

    context = {'form': form}
    data['html_form'] = render_to_string('obstetricia/index_obs2.html',
        context,
        request=request,
    )
    return JsonResponse(data)

#Vistas del modal de edicion

@login_required
def edit_paciente(request,pk):
    formatted_date = dateformat.format(timezone.now(), 'Y-m-d h:m:s')
    edit = get_object_or_404(Parto,pk=pk)
    edit2 = get_object_or_404(Antecedentes,pk=pk)
    data = dict()
    if request.method == 'POST':
        form = PartoForm(request.POST,instance=edit)
        form2 = AntecedentesForm(request.POST,instance=edit2) 
        if form.is_valid():
            tipo = Paciente_obstetricia.objects.get(pk = request.POST['ci_paciente'])
            exito = form.save(commit=False)
            exito2 = form2.save(commit=False)
            exito.fecha = formatted_date
            exito.save()
            exito2.ci_paciente = tipo
            exito2.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = PartoForm(instance=edit)
        form2 = AntecedentesForm(instance=edit2)

    context = {'form': form,'form2':form2}
    data['html_form'] = render_to_string('obstetricia/edit_paciente.html',context,request=request)
    return JsonResponse(data)
    
#vista del modal de eliminar
@login_required
def eliminar_paciente(request,pk,pk2):
    paciente = get_object_or_404(Paciente_obstetricia, pk=pk2)
    parto = get_object_or_404(Parto, pk=pk)
    inst = Parto.objects.filter(id_historia_parto=pk).exists()
    inst2 = Antecedentes.objects.filter(id_antecedentes=pk).exists()
    inst3 = Nota.objects.filter(id_historia_nota_parto=pk).exists()
    inst4 = Orden_medica_parto.objects.filter(id_orden_medica_parto=pk).exists()
    inst5 = Examen_fisico.objects.filter(id_examen_fisico=pk).exists()
    data = dict()
    if request.method == 'POST':
        if inst == True:
            instancia = Parto.objects.get(id_historia_parto=pk) 
            instancia.delete()        
        else:
            print("no")
        if inst2 == True:
            instancia2 = Antecedentes.objects.get(id_antecedentes=pk)
            instancia2.delete()
        else:
            print("no")
        if inst3 == True:
            instancia3 = Nota.objects.get(id_historia_nota_parto=pk) 
            instancia3.delete()        
        else:
            print("no")
        if inst4 == True:
            instancia4 = Orden_medica_parto.objects.get(id_orden_medica_parto=pk)
            instancia4.delete()         
        else:
            print("no")
        if inst5 == True:
            instancia5 = Examen_fisico.objects.get(id_examen_fisico=pk)
            instancia5.delete()         
        else:
            print("no")

        data['form_is_valid'] = True  # This is just to play along with the existing code
        return redirect('buscar_obs')
    else:
        context = {'paciente':paciente,'parto':parto}
        data['html_form'] = render_to_string('obstetricia/eliminar_paciente.html',
            context,
            request=request,
        )
    return JsonResponse(data)




#Generando el reporte en un pdf con reportlab


@login_required
def reporte_historia(request,pk=None,pk2=None):
    if not pk and cedula:
        print("No hay paciente con ese numero de id y cedula")
    else:
        paciente = Paciente_obstetricia.objects.filter(id=pk)
        parto = Parto.objects.filter(id_historia_parto=pk2)
        ante = Antecedentes.objects.filter(id_antecedentes=pk2)
        
        for p in paciente:
            for pp in parto:
                for pa in ante:
                    if pa.aco == True:
                        pa.aco = "Si"
                    else:
                        pa.aco = "No"
                    if pa.citologia == True:
                        pa.citologia = "Si"
                    else:
                        pa.citologia = "No"
                    if pa.its == True:
                        pa.its = "Si"
                    else:
                        pa.its = "No"
                    if pa.diu == True:
                        pa.diu = "Si"
                    else:
                        pp.diu = "No"
                    if pp.deseado == True:
                        pp.deseado = "Si"
                    else:
                        pp.deseado = "No"
                    if pp.planificado == True:
                        pp.planificado = "Si"
                    else:
                        pp.planificado = "No"
                    if pp.controlado == True:
                        pp.controlado = "Si"
                    else:
                        pp.controlado = "No"
                    if pp.itu == True:
                        pp.itu = "Si"
                    else:
                        pp.itu = "No"
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=Historia_Clinica_Ci:%s.pdf'% p.cedula
                    buff = BytesIO()
                    doc = SimpleDocTemplate(buff,pagesize=letter)
                    Story = []
                    
                    h1 = PS(name = 'Heading1',fontSize = 25,leading = 16,alignment=TA_CENTER,fontName="Times-Roman")
                    h2 = PS(name = 'Heading1',fontSize = 14, leading = 14,fontName="Times-Roman")
                    h3 = PS(name='parrafos_normales',fontSize=12,fontName="Times-Roman",alignment=TA_JUSTIFY)
                    h4 = PS(name='parrafos_centrados',fontSize=12,fontName="Times-Roman",alignment=TA_CENTER)
                    h5 = PS(name='parrafos_derechos',fontSize=12,fontName="Times-Roman",alignment=TA_RIGHT)
                    
                    texto = 'Hospital "Pablo Acosta Ortiz"'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1, 0))
                    texto =  "Servicio de Sala de Parto 5to Piso"
                    Story.append(Paragraph(texto, h5))
                    texto = '%s' % pp.fecha
                    Story.append(Paragraph(texto,h5))
                    texto = 'Numero de Historia: %s' % pp.id_historia_parto
                    Story.append(Paragraph(texto,h5))
                    logotipo =settings.BASE_DIR+'/obstetricia/static/img/logo1.png'   
                    imagen = Image(logotipo, 2 * inch, 1 * inch, hAlign='LEFT')    
                    Story.append(imagen)


                    texto = 'Historia Clinica'
                    Story.append(Paragraph(texto, h1))
                    Story.append(Spacer(1, 12))

                    
                    texto = 'Motivo de Consulta: %s' % pp.motivo_consulta
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1, 12))
                    
                    texto = 'Paciente:  %s %s \
                            Cedula: %s \
                            Telefono: %s ' % (p.nombre,p.apellido,p.cedula,p.telefono) 
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    
                    texto = u'Enfermedad actual se trata de una gestante de %s años, natural y procedente:  %s \
                            con FUR: %s , %s gestas, %s partos, %s cesareas, %s legrados, quien acude a consulta por presentar %s motivo por el \
                            cual se evalua y se decide su ingreso.'%(p.edad,p.direccion,pa.fur,pa.gestas,pa.partos,pa.cesareas,pa.legrados,pp.presenta)
                    
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = 'Diagnostico: '
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1, 8))
                    texto = '%s' % pp.diagnostico
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = 'Antecedentes Familiares.'
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1, 12))
                    if len(pa.antemadre) < 5 and len(pa.antepadre) < 5 :
                        texto = "#.-Madre: %s.    #.-Padre: %s"% (pa.antemadre,pa.antepadre)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                    else:
                        texto = "#.-Madre: %s."% (pa.antemadre)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                        texto = "#.-Padre: %s."% (pa.antepadre)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                    if len(pa.antehermanos) < 5 and len(pa.antehijos):
                        texto = "#.-Hermanos: %s.    #.-Hijos: %s"% (pa.antehermanos,pa.antehijos)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                    else:
                        texto = "#.-Hermanos: %s."% (pa.antehermanos)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                        texto = "#.-Hijos: %s."% (pa.antehijos)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))

                    texto = 'Antecedentes Personales.'
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1, 8))
                    if len(pa.patologias) < 5 and len(pa.alergias) < 5:
                        texto = '#.-Patologia Base: %s. #.-Alergia a Medicamentos: %s ' % (pa.patologias,pa.alergias)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                    else:
                        texto = "#.-Patologia Base: %s."% (pa.patologias)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                        texto = "#.-Alergia a Medicamentos: %s."% (pa.alergias)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                    if len(pa.transfusiones) < 5 and len(pa.intervenciones) < 5:
                        texto = "#.-Transfuciones Sanguineas: %s. #.-Intervenciones Quirurgicas: %s." % (pa.transfusiones,pa.intervenciones)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 8))
                    else:
                        texto = "#.-Transfuciones Sanguineas: %s."% (pa.transfusiones)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))
                        texto = "#.-Intervenciones Quirurgicas: %s."% (pa.intervenciones)
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 7))

                    texto = 'Antecedentes Gineco-Obstetricos.'
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1, 8))

                    texto = u'#.-Menarquia: %s años. #.-Sexarquia: %s años.' % (pa.menarquia,pa.sexarquia)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 7))
                    texto = "#.-FUR: %s. #.-Ciclo Menstrual: %s"  % (pa.fur,pa.ciclomens)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 7))
                    texto = '#.-Numero de parejas: %s. #.-Aco: %s '% (pa.parejas,pa.aco)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 7))
                    texto = "#.-Citologia: %s. #.-Its: %s" % (pa.citologia,pa.its)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 7))
                    texto = "#.-Diu: %s." % pa.diu
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = 'Embarazo Anterior.'
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1,12))
                    texto = '%s' % pa.embarazo_ante
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12 ))
                    texto = ' ' 
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12 ))
                    

                    texto = 'Embarazo Actual.'
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1,7))
                    texto = "#.-Deseado: %s. #.-Planificado: %s" % (pp.deseado,pp.planificado)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 7))
                    texto = "#.-Controlado: %s. #.-Itu: %s" % (pp.controlado,pp.itu)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 7))
                    texto = "#.-Numero de Controles: %s." % pp.controles
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = 'Laboratorio: %s .' % pp.laboratorio
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1,12))
                    if pp.genero == "Hombre":
                        texto = 'Dr. %s %s'%(pp.medico_nombre,pp.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(pp.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    elif pp.genero == "":
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    else:
                        texto = 'Dra. %s %s'%(pp.medico_nombre,pp.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(pp.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))

                    doc.build(Story)
                    pdf = buff.getvalue()
                    response.write(pdf)
                    buff.close()
                    return response


@login_required
def reporte_consentimiento(request,pk=None,pk2=None):
    if not pk:
        print("No hay paciente con ese numero de id")
    else:
        paciente = Paciente_obstetricia.objects.filter(id=pk)
        parto = Parto.objects.filter(id_historia_parto=pk2)
        for p in paciente:
            for pp in parto:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=Consentimiento_Informado_Ci:%s.pdf'% p.cedula
                buff = BytesIO()
                doc = SimpleDocTemplate(buff,pagesize=letter)
                Story = []
                
                h1 = PS(name = 'Heading1',fontSize = 25,leading = 16,alignment=TA_CENTER,fontName="Times-Roman")
                h2 = PS(name = 'Heading1',fontSize = 14, leading = 14,fontName="Times-Roman")
                h3 = PS(name='parrafos_normales',fontSize=12,fontName="Times-Roman",alignment=TA_JUSTIFY)
                h4 = PS(name='parrafos_centrados',fontSize=12,fontName="Times-Roman",alignment=TA_CENTER)
                h5 = PS(name='parrafos_derechos',fontSize=12,fontName="Times-Roman",alignment=TA_RIGHT)
                
                texto = 'Hospital "Pablo Acosta Ortiz"'
                Story.append(Paragraph(texto, h5))
                Story.append(Spacer(1, 0))
                texto =  "Servicio de Sala de Parto 5to Piso"
                Story.append(Paragraph(texto, h5))
                texto = '%s' % pp.fecha
                Story.append(Paragraph(texto,h5))
                texto = 'Numero de Historia: %s' % pp.id_historia_parto
                Story.append(Paragraph(texto,h5))
                logotipo =settings.BASE_DIR+'/obstetricia/static/img/logo1.png'   
                imagen = Image(logotipo, 2 * inch, 1 * inch, hAlign='LEFT')    
                Story.append(imagen)

                texto = 'Consentimiento Informado'
                Story.append(Paragraph(texto, h1))
                Story.append(Spacer(1, 15))
                
                texto = u'Dando Cumplimiento al articulo N# 34 de la ley \
                        del ejercicio de la medicina yo : %s %s , Titular de la CI: %s . '%(p.nombre,p.apellido,p.cedula)
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1, 12))

                texto = u'Habiendo sido informada de forma, clara y oportuna y suficiente \
                        de las condiciones que presento y habiendo entendido los riesgos y beneficios \
                        potenciales, autorizo al personal medico y de enfermeria que prestan sus servicios\
                        en el Hospital Pablo Acosta Ortiz a realizar todos los actos que consideren necesarios\
                        para la antencion del mismo incluyendo la administracion de medicamentos y cirugias, asi como tambien \
                        el acto anestesico en caso de ser necesario '
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1, 12))

                texto = 'Diagnostico.'
                Story.append(Paragraph(texto, h2))
                Story.append(Spacer(1, 12))

                texto = '%s' % pp.diagnostico
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1, 12))

                texto = 'Paciente: %s %s' % (p.nombre,p.apellido)
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1,7))
                texto = 'Cedula: %s' % p.cedula
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1,7))
                texto = 'Firma.' 
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1,7))

                texto = 'Familiar:'
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1,7))
                texto = 'CI:' 
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1,7))
                texto = 'Firma.' 
                Story.append(Paragraph(texto, h3))
                Story.append(Spacer(1,7))
                if pp.genero == "Hombre":
                    texto = 'Dr. %s %s'%(pp.medico_nombre,pp.medico_apellido)
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))
                    texto = '%s'%(pp.rango)
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))
                    texto = 'Firma y Sello.'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))
                elif pp.genero == "":
                    texto = 'Firma y Sello.'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))
                else:
                    texto = 'Dra. %s %s'%(pp.medico_nombre,pp.medico_apellido)
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))
                    texto = '%s'%(pp.rango)
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))
                    texto = 'Firma y Sello.'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1,7))


                doc.build(Story)
                pdf = buff.getvalue()
                response.write(pdf)
                buff.close()
                return response

@login_required
def reporte_nota(request,pk=None,pk2=None):
    try:
        if not pk:
            print("No hay paciente con ese numero de id")
        else:
            paciente_nota = Nota.objects.filter(id_historia_nota_parto=pk2)
            paciente = Paciente_obstetricia.objects.filter(id=pk)
            for p in paciente:
                for pn in paciente_nota:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=Nota_Parto_Ci:%s.pdf'% p.cedula
                    buff = BytesIO()
                    doc = SimpleDocTemplate(buff,pagesize=letter)
                    Story = []
                    
                    h1 = PS(name = 'Heading1',fontSize = 25,leading = 16,alignment=TA_CENTER,fontName="Times-Roman")
                    h2 = PS(name = 'Heading1',fontSize = 14, leading = 14,fontName="Times-Roman")
                    h3 = PS(name='parrafos_normales',fontSize=12,fontName="Times-Roman",alignment=TA_JUSTIFY)
                    h4 = PS(name='parrafos_centrados',fontSize=12,fontName="Times-Roman",alignment=TA_CENTER)
                    h5 = PS(name='parrafos_derechos',fontSize=12,fontName="Times-Roman",alignment=TA_RIGHT)
                    
                    texto = 'Hospital "Pablo Acosta Ortiz"'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1, 0))
                    texto =  "Servicio de Sala de Parto 5to Piso"
                    Story.append(Paragraph(texto, h5))
                    texto = '%s' % pn.fecha
                    Story.append(Paragraph(texto,h5))
                    texto = 'Numero de Historia: %s' % pn.id_historia_nota_parto
                    Story.append(Paragraph(texto,h5))
                    logotipo =settings.BASE_DIR+'/obstetricia/static/img/logo1.png'   
                    imagen = Image(logotipo, 2 * inch, 1 * inch, hAlign='LEFT')    
                    Story.append(imagen)

                    texto = 'Nota de Parto.'
                    Story.append(Paragraph(texto, h1))
                    Story.append(Spacer(1, 15))

                    texto = 'Paciente:  %s %s \
                            Cedula: %s ' % (p.nombre,p.apellido,p.cedula) 
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    
                    texto = u'1.- %s .'% pn.nota_uno
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'2.- %s .'% pn.nota_dos
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'3.- %s .'% pn.nota_tres
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'4.- %s .'% pn.nota_cuatro
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'5.- %s .'% pn.nota_cinco
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'6.- %s .'% pn.nota_seis
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'7.- %s .'% pn.nota_siete
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'8.- %s .'% pn.nota_ocho
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    if pn.nota_nueve == "":
                        texto = ""
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1,1))
                    else:
                        texto = u'9.- %s .'% pn.nota_nueve
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 12))
                    if pn.nota_diez == "":
                        texto = ""
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1,1))
                    else:
                        texto = u'10.- %s .'% pn.nota_diez
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 12))

                    texto = 'Diagnostico.'
                    Story.append(Paragraph(texto, h2))
                    Story.append(Spacer(1, 12))

                    texto = '%s' % pn.diagnostico2
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    if pn.genero == "Hombre":
                        texto = 'Dr. %s %s'%(pn.medico_nombre,pn.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(pn.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    elif pn.genero == "":
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    else:
                        texto = 'Dra. %s %s'%(pn.medico_nombre,pn.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(pn.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    doc.build(Story)
                    pdf = buff.getvalue()
                    response.write(pdf)
                    buff.close()
                    return response
    except Nota.DoesNotExist:
        raise Http404("La nota no existe, cree una nota para el paciente ")

    return redirect('nota_parto')

@login_required
def reporte_orden(request,pk=None,pk2=None):
    try:
        if not pk:
            print("No hay paciente con ese numero de id")
        else:
            paciente_orden = Orden_medica_parto.objects.filter(id_orden_medica_parto=pk2)
            paciente = Paciente_obstetricia.objects.filter(id=pk)
            for p in paciente:
                for po in paciente_orden:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=Orden_medica_Parto_Ci:%s.pdf'% p.cedula
                    buff = BytesIO()
                    doc = SimpleDocTemplate(buff,pagesize=letter)
                    Story = []
                    
                    h1 = PS(name = 'Heading1',fontSize = 25,leading = 16,alignment=TA_CENTER,fontName="Times-Roman")
                    h2 = PS(name = 'Heading1',fontSize = 14, leading = 14,fontName="Times-Roman")
                    h3 = PS(name='parrafos_normales',fontSize=12,fontName="Times-Roman",alignment=TA_JUSTIFY)
                    h4 = PS(name='parrafos_centrados',fontSize=12,fontName="Times-Roman",alignment=TA_CENTER)
                    h5 = PS(name='parrafos_derechos',fontSize=12,fontName="Times-Roman",alignment=TA_RIGHT)
                    
                    texto = 'Hospital "Pablo Acosta Ortiz"'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1, 0))
                    texto =  "Servicio de Sala de Parto 5to Piso"
                    Story.append(Paragraph(texto, h5))
                    texto = '%s' % po.fecha
                    Story.append(Paragraph(texto,h5))
                    texto = 'Numero de Historia: %s' % po.id_orden_medica_parto
                    Story.append(Paragraph(texto,h5))
                    logotipo =settings.BASE_DIR+'/obstetricia/static/img/logo1.png'   
                    imagen = Image(logotipo, 2 * inch, 1 * inch, hAlign='LEFT')    
                    Story.append(imagen)

                    texto = 'Orden Medica de Parto.'
                    Story.append(Paragraph(texto, h1))
                    Story.append(Spacer(1, 15))

                    texto = 'Paciente:  %s %s \
                            Cedula: %s ' % (p.nombre,p.apellido,p.cedula) 
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    
                    texto = u'1.- %s .'% po.orden_uno
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'2.- %s .'% po.orden_dos
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'3.- %s .'% po.orden_tres
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'4.- %s .'% po.orden_cuatro
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'5.- %s .'% po.orden_cinco
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'6.- %s .'% po.orden_seis
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    texto = u'7.- %s .'% po.orden_siete
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))

                    if po.orden_ocho == "":
                        texto = ""
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1,1))
                    else:
                        texto = u'8.- %s .'% po.orden_ocho
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 12))
                    if po.orden_nueve == "":
                        texto = ""
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 1))
                    else:
                        texto = u'9.- %s .'% po.orden_nueve
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 12))
                    
                    if po.orden_diez == "":
                        texto = ""
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 1))
                    else:
                        texto = u'10.- %s .'% po.orden_nueve
                        Story.append(Paragraph(texto, h3))
                        Story.append(Spacer(1, 12))

                    if po.genero == "Hombre":
                        texto = 'Dr. %s %s'%(po.medico_nombre,po.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(po.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    elif po.genero == "":
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    else:
                        texto = 'Dra. %s %s'%(po.medico_nombre,po.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(po.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))

                    doc.build(Story)
                    pdf = buff.getvalue()
                    response.write(pdf)
                    buff.close()
                    return response
    except Nota.DoesNotExist:
        raise Http404("La orden medica no existe, cree una orden medica para el paciente ")

    return redirect('orden_medica_parto')


@login_required
def reporte_examen_fisico(request,pk=None,pk2=None):
    try:
        if not pk:
            print("No hay paciente con ese numero de id")
        else:
            paciente = Paciente_obstetricia.objects.filter(id=pk)
            examen_fisico = Examen_fisico.objects.filter(id_examen_fisico=pk2)
            for p in paciente:
                for pp in examen_fisico:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=Examen_Fisco_Ci:%s.pdf'% p.cedula
                    buff = BytesIO()
                    doc = SimpleDocTemplate(buff,pagesize=letter)
                    Story = []
                    
                    h1 = PS(name = 'Heading1',fontSize = 25,leading = 16,alignment=TA_CENTER,fontName="Times-Roman")
                    h2 = PS(name = 'Heading1',fontSize = 14, leading = 14,fontName="Times-Roman")
                    h3 = PS(name='parrafos_normales',fontSize=12,fontName="Times-Roman",alignment=TA_JUSTIFY)
                    h4 = PS(name='parrafos_centrados',fontSize=12,fontName="Times-Roman",alignment=TA_CENTER)
                    h5 = PS(name='parrafos_derechos',fontSize=12,fontName="Times-Roman",alignment=TA_RIGHT)
                    
                    texto = 'Hospital "Pablo Acosta Ortiz"'
                    Story.append(Paragraph(texto, h5))
                    Story.append(Spacer(1, 0))
                    texto =  "Servicio de Sala de Parto 5to Piso"
                    Story.append(Paragraph(texto, h5))
                    texto = '%s' % pp.fecha
                    Story.append(Paragraph(texto,h5))
                    texto = 'Numero de Historia: %s' % pp.id_examen_fisico
                    Story.append(Paragraph(texto,h5))
                    logotipo =settings.BASE_DIR+'/obstetricia/static/img/logo1.png'   
                    imagen = Image(logotipo, 2 * inch, 1 * inch, hAlign='LEFT')    
                    Story.append(imagen)

                    texto = 'Examen Fisico'
                    Story.append(Paragraph(texto, h1))
                    Story.append(Spacer(1, 12))
                    
                    texto = u'Signo Vitales. T/A:%s,  FC: %s, FR:%s.'%(pp.ta,pp.fc,pp.fr)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    texto = u'Cardio-Pulmonar: %s.'% pp.cardio_pul
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    texto = 'Mamas: %s.'% pp.mamas
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    texto = 'Abdomen: %s.' % pp.abdomen
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1, 12))
                    texto = 'Feto: %s.' % (pp.feto)
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12))
                    texto = 'Normoconfigurados: %s.' % pp.normoconfigurados
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12))
                    texto = 'Cuello Uterino: %s.' % pp.cuello_uterino
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12))
                    texto = 'Extremidades Inferiores: %s.' % pp.extremidades
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12))
                    texto = 'Neurologico: %s.' % pp.neurologico
                    Story.append(Paragraph(texto, h3))
                    Story.append(Spacer(1,12))
                    
                    if pp.genero == "Hombre":
                        texto = 'Dr. %s %s'%(pp.medico_nombre,pp.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(pp.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    elif pp.genero == "":
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                    else:
                        texto = 'Dra. %s %s'%(pp.medico_nombre,pp.medico_apellido)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = '%s'%(pp.rango)
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))
                        texto = 'Firma y Sello.'
                        Story.append(Paragraph(texto, h5))
                        Story.append(Spacer(1,7))


                    doc.build(Story)
                    pdf = buff.getvalue()
                    response.write(pdf)
                    buff.close()
                    return response
    except Nota.DoesNotExist:
        raise Http404("La Examen Fisico no existe, cree un registro de examen fisico para el paciente ")

    return redirect('examen_fisico')