import datetime

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from itertools import islice, chain
from estudiante.models import Taller,Curso,Academic_Rank,TallerGeneral
from contrato.models import Estudiante
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_user(request):
    state = "Por favor ingrese a continuacion"
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "Conectado con exito"
                usuario = User.objects.get(username=username)
                fotourl = usuario.estudiante.foto.url
                cedula = usuario.estudiante.cedula
                telefono = usuario.estudiante.telefono
                fecha = datetime.datetime.today()
                programa = usuario.estudiante.programa.nombre_del_programa
                duracion = usuario.estudiante.fecha_de_expiracion
                startdate = datetime.date.today()+ datetime.timedelta(days=1)
                enddate = startdate + datetime.timedelta(days=6)
                nivel  = usuario.estudiante.nivel
                cursos = []
                talleres = []
                if Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).count() > 0 :
                    cursos1 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_leccion__in=range(usuario.estudiante.nivel.leccion-5,usuario.estudiante.nivel.leccion+6)).\
                        filter(tipo_nivel=usuario.estudiante.nivel.nivel).filter(sede=usuario.estudiante.sede).exclude(tipo_nivel='xx')
                    cursos2 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_nivel='xx').filter(sede=usuario.estudiante.sede)
                    cursos = list(chain(cursos1,cursos2))
                    print cursos
                talleres = Taller.objects.filter(nivel=usuario.estudiante.nivel.nivel).filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
                talleresg = TallerGeneral.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
                print talleres
                # .filter(hora_inicio__gt=time.strftime("%H:%M:%S"))
                return render(request,'contenido.html',{'username':username,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel})
            else:
                state = "Tu cuenta esta desactivada por favor acercarce a oficinas."
        else:
            state = "Usuario o contrasena incorrecta"

    return render(request,'signin.html',{'state':state}, context_instance=RequestContext(request))

def cuenta(request):
    state = "Conectado con exito"
    user = request.user.id
    print 'Imprimiendo en usuario'
    print user
    usuario = User.objects.get(id=user)
    print usuario
    fotourl = usuario.estudiante.foto.url
    cedula = usuario.estudiante.cedula
    telefono = usuario.estudiante.telefono
    fecha = datetime.datetime.today()
    programa = usuario.estudiante.programa.nombre_del_programa
    duracion = usuario.estudiante.fecha_de_expiracion
    startdate = datetime.date.today()+ datetime.timedelta(days=1)
    enddate = startdate + datetime.timedelta(days=6)
    nivel  = usuario.estudiante.nivel
    cursos = []
    talleres = []
    if Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).count() > 0 :
        cursos1 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
        filter(tipo_leccion__in=range(usuario.estudiante.nivel.leccion-5,usuario.estudiante.nivel.leccion+6)).\
        filter(tipo_nivel=usuario.estudiante.nivel.nivel).filter(sede=usuario.estudiante.sede)
        cursos2 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                    filter(tipo_nivel='xx').filter(sede=usuario.estudiante.sede)
        cursos = list(chain(cursos1,cursos2))
        print cursos
    talleresg = TallerGeneral.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
    talleres = Taller.objects.filter(nivel=usuario.estudiante.nivel.nivel).filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
    print talleres
        # .filter(hora_inicio__gt=time.strftime("%H:%M:%S"))
    return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel})

class Busqueda_info_ajax(TemplateView):
    def get(self, request, *args, **kwargs):
        id_taller = request.GET['id']
        print id_taller
        info = Taller.objects.filter(id=id_taller)
        data=serializers.serialize("json", info)
        print data
        return HttpResponse(data, content_type="application/json")

@login_required
def reserva(request):
    estado = False
    if request.method == 'POST':
        user = request.user.id
        usuario = User.objects.get(id=user)
        fotourl = usuario.estudiante.foto.url
        cedula = usuario.estudiante.cedula
        telefono = usuario.estudiante.telefono
        fecha = datetime.datetime.today()
        programa = usuario.estudiante.programa.nombre_del_programa
        duracion = usuario.estudiante.fecha_de_expiracion
        startdate = datetime.date.today()+ datetime.timedelta(days=1)
        enddate = startdate + datetime.timedelta(days=6)
        nivel  = usuario.estudiante.nivel
        cursos = []
        talleres = []
        taller = request.POST.get('talleres')
        taller_actualizar = Taller.objects.get(pk=taller)
        if Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).count() > 0 :
            cursos1 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_leccion__in=range(usuario.estudiante.nivel.leccion-5,usuario.estudiante.nivel.leccion+6)).\
                        filter(tipo_nivel=usuario.estudiante.nivel.nivel).filter(sede=usuario.estudiante.sede)
            cursos2 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_nivel='xx').filter(sede=usuario.estudiante.sede)
            cursos = list(chain(cursos1,cursos2))
            print cursos
        talleres = Taller.objects.filter(nivel=usuario.estudiante.nivel.nivel).filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
        print talleres
        talleresg = TallerGeneral.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
        if taller_actualizar.estudiantes.all().filter(pk=usuario.estudiante.cedula).count() == 0:
            taller_actualizar.estudiantes.add(usuario.estudiante)

            taller_actualizar.capacidad = taller_actualizar.capacidad - 1
            taller_actualizar.save()
            estado = True
            return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado1':estado})
        else:
            return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado1':estado})
    else:
        return render(request,'contenido.html',{'estado':estado})
@login_required
def reservar_curso(request):
    estado = False
    if request.method == 'POST':
        user = request.user.id
        usuario = User.objects.get(id=user)
        fotourl = usuario.estudiante.foto.url
        cedula = usuario.estudiante.cedula
        telefono = usuario.estudiante.telefono
        fecha = datetime.datetime.today()
        programa = usuario.estudiante.programa.nombre_del_programa
        duracion = usuario.estudiante.fecha_de_expiracion
        startdate = datetime.date.today()+ datetime.timedelta(days=1)
        enddate = startdate + datetime.timedelta(days=6)
        nivel  = usuario.estudiante.nivel
        cursos = []
        talleres = []
        curso = request.POST.get('cursos')
        curso_actualizar = Curso.objects.get(pk=curso)
        if Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).count() > 0 :
            cursos1 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_leccion__in=range(usuario.estudiante.nivel.leccion-5,usuario.estudiante.nivel.leccion+6)).\
                        filter(tipo_nivel=usuario.estudiante.nivel.nivel).filter(sede=usuario.estudiante.sede)
            cursos2 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_nivel='xx').filter(sede=usuario.estudiante.sede)
            cursos = list(chain(cursos1,cursos2))
            print cursos
        talleres = Taller.objects.filter(nivel=usuario.estudiante.nivel.nivel).filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
        talleresg = TallerGeneral.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
        print talleres
        if curso_actualizar.tipo_nivel == 'xx' or curso_actualizar.tipo_leccion == 0:
            curso_actualizar.tipo_nivel = usuario.estudiante.nivel.nivel
            curso_actualizar.tipo_leccion = usuario.estudiante.nivel.leccion
            curso_actualizar.save()
        curso_actualizar = Curso.objects.get(pk=curso)
        if curso_actualizar.tipo_estudiante.count()< curso_actualizar.max_tipo:
            if curso_actualizar.estudiantes.all().filter(pk=usuario.estudiante.cedula).count() == 0:
                usuario.estudiante.nivel.leccion = usuario.estudiante.nivel.leccion + 1
                curso_actualizar.estudiantes.add(usuario.estudiante)
                curso_actualizar.capacidad_maxima = curso_actualizar.capacidad_maxima - 1
                curso_actualizar.tipo_estudiante.add(usuario.estudiante.nivel)
                curso_actualizar.save()
                estado = True
                return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado':estado})
            else:
                return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado':estado})
        else:
            return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado':estado})
    else:
        return render(request,'contenido.html',{'estado:':estado})


@login_required
def reservaTaller(request):
    estadoTaller = False
    if request.method == 'POST':
        user = request.user.id
        usuario = User.objects.get(id=user)
        fotourl = usuario.estudiante.foto.url
        cedula = usuario.estudiante.cedula
        telefono = usuario.estudiante.telefono
        fecha = datetime.datetime.today()
        programa = usuario.estudiante.programa.nombre_del_programa
        duracion = usuario.estudiante.fecha_de_expiracion
        startdate = datetime.date.today()+ datetime.timedelta(days=1)
        enddate = startdate + datetime.timedelta(days=6)
        nivel  = usuario.estudiante.nivel
        cursos = []
        talleres = []
        taller = request.POST.get('talleresg')
        taller_actualizar = TallerGeneral.objects.get(pk=taller)
        if Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).count() > 0 :
            cursos1 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_leccion__in=range(usuario.estudiante.nivel.leccion-5,usuario.estudiante.nivel.leccion+6)).\
                        filter(tipo_nivel=usuario.estudiante.nivel.nivel).filter(sede=usuario.estudiante.sede)
            cursos2 = Curso.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad_maxima__gt=0).\
                        filter(tipo_nivel='xx').filter(sede=usuario.estudiante.sede)
            cursos = list(chain(cursos1,cursos2))
            print cursos
        talleres = Taller.objects.filter(nivel=usuario.estudiante.nivel.nivel).filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
        talleresg = TallerGeneral.objects.filter(fecha__range=[startdate, enddate]).filter(capacidad__gt=0).filter(lugar=usuario.estudiante.sede)
        print talleres
        if taller_actualizar.alumnos.all().filter(pk=usuario.estudiante.cedula).count() == 0:
            taller_actualizar.alumnos.add(usuario.estudiante)
            taller_actualizar.capacidad = taller_actualizar.capacidad - 1
            taller_actualizar.save()
            estadoTaller = True
            return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado1':estadoTaller})
        else:
            return render(request,'contenido.html',{'username':request.user,'fecha':fecha,'duracion':duracion,'fotourl':fotourl,'cedula':cedula,'telefono':telefono,'programa':programa,'talleres':talleres,'talleresg':talleresg,'cursos':cursos,'nivel':nivel,'estado1':estadoTaller})
    else:
        return render(request,'contenido.html',{'estado':estadoTaller})



def update(request, pullo):
    if request.method == 'POST':
        user = request.user.id
        taller = Taller.objects.get(pk=pullo)
        print user
        print taller
        return HttpResponseRedirect('/clientes/')
    else:

        return render_to_response('account.html')
@login_required
def academic_rank(request):
    user = request.user.id
    usuario = User.objects.get(id=user)
    estudiante = Estudiante.objects.get(pk=usuario.estudiante.cedula)
    nivel  = usuario.estudiante.nivel
    print estudiante
    academic = []
    academic = Academic_Rank.objects.all().filter(estudiante=estudiante)
    print academic
    if academic.count() > 0:

        return  render(request,'rank.html',{'academic':academic,'username':request.user,'duracion':estudiante.fecha_de_expiracion,'fotourl':estudiante.foto.url,'cedula':estudiante.cedula,'telefono':estudiante.telefono,'programa':estudiante.programa,'nivel':nivel})
    else:
        return render(request,'rank.html',{'academic':academic}, context_instance=RequestContext(request))




# def buscar(request):
#     context_instance= RequestContext(request)
#     if 'talleres' in request.GET and request.GET['talleres']:
#         mensaje = 'Estas buscando: %r' % request.GET['talleres']
#         print request.user
#         print request.user.username
#     else:
#         mensaje = 'Haz subido un formulario vacio.'
#     return HttpResponse(mensaje)

# def reservaTaller(request):
#     if request.POST:
#         form = TalleresForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/')
#     else:
#         form = TalleresForm()
#     args = {}
#     args.update(csrf(request))
#     args['form'] = form
#     return render_to_response('talleres.html', args)
#
# class reservaTallerView(UpdateView):
#     model = Taller
#     template_name = 'talleres.html'
#     form_class = TalleresForm
#     success_url = '/'