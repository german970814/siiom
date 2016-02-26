# -*- coding: utf-8 -*- 
# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth, messages
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from miembros.forms import *
from grupos.models import Grupo
from datetime import date
from academia.views import adminTest
from academia.models import Curso
import datetime
from django.core.mail import send_mail
from django.db.models.aggregates import Count

def eliminar(modelo, lista):
    ok = 0 #No hay nada en la lista
    if lista:
        ok = 1 #Los borro todos
        for e in lista:
            try:
                modelo.objects.get(id=e).delete()
            except:
                ok = 2 #Hubo un error
    return ok

def autenticarUsario(request):
    algo = request.GET.get('next','')
    request.session['next'] = request.GET.get('next')

    if request.user.is_authenticated():
        if request.user.has_perm("miembros.es_administrador"):
            return HttpResponseRedirect("/administracion/") 
        else:
            return HttpResponseRedirect("/miembro/")

    valido = True
    if request.method == 'POST':
        nombreUsuaroio = request.POST.get('username', '')
        contrasena = request.POST.get('password', '')
        sig = request.POST.get('next','')
        usuario = auth.authenticate(username=nombreUsuaroio, password=contrasena)
        if usuario is not None:
            auth.login(request, usuario)
            if  Group.objects.get(name__iexact='Administrador') in usuario.groups.all():
                if sig != None or sig != '':
                    return HttpResponseRedirect(sig)
                return HttpResponseRedirect("/miembro/")
            elif Group.objects.get(name__iexact='Lider') in usuario.groups.all()      \
                    or Group.objects.get(name__iexact='Maestro') in usuario.groups.all()\
                    or Group.objects.get(name__iexact='Agente') in usuario.groups.all()\
                    or Group.objects.get(name__iexact='Receptor') in usuario.groups.all():
                    if sig != None or sig != '':
                        return HttpResponseRedirect(sig)
                    return HttpResponseRedirect('/miembro/')
            else:
                valido = False
        else:
            valido = False
    return render_to_response('Miembros/login.html', locals(), context_instance=RequestContext(request))

def salir(request):
    auth.logout(request)
    return HttpResponseRedirect('/iniciar_sesion')

def miembroTest(user):
    return  user.is_authenticated() \
            and (Group.objects.get(name__iexact='Maestro') in user.groups.all()\
            or Group.objects.get(name__iexact='Lider') in user.groups.all()    \
            or Group.objects.get(name__iexact='Agente') in user.groups.all()   \
            or Group.objects.get(name__iexact='Receptor') in user.groups.all()
            or Group.objects.get(name__iexact='Administrador') in user.groups.all())
        
def liderTest(user):
    return  user.is_authenticated() \
            and Group.objects.get(name__iexact='Lider') in user.groups.all()
            
def agenteTest(user):
    return  user.is_authenticated() \
            and Group.objects.get(name__iexact='Agente') in user.groups.all()            
            
def editarMiembroTest(user):
    return  user.is_authenticated() \
            and user.has_perm("miembros.puede_editar_miembro")
            
def llamdaAgenteTest(user):
    return  user.is_authenticated() \
            and user.has_perm("miembros.llamada_agente")

def agregarVisitanteTest(user):
    return  user.is_authenticated() \
            and user.has_perm("miembros.puede_agregar_visitante")

def cumplimientoPasosTest(user):
    return  user.is_authenticated() \
            and user.has_perm("miembros.cumplimiento_pasos")

def asignarGrupoTest(user):
    return  user.is_authenticated()\
            and (Group.objects.get(name__iexact='Agente') in user.groups.all()\
             or Group.objects.get(name__iexact='Administrador') in user.groups.all())
            
@user_passes_test(miembroTest, login_url="/iniciar_sesion/")
def miembroInicio(request):
    miembro = Miembro.objects.get(usuario = request.user)
    grupo = miembro.grupoLidera()
    if grupo:
        miembrosGrupo = list(grupo.miembro_set.all())
        tipo = TipoMiembro.objects.get(nombre__iexact = 'visita')
        visitantes = []
        for mg in miembrosGrupo:
            ct = list(CambioTipo.objects.filter(miembro = mg).order_by('id'))#.filter(nuevoTipo=tipo, anteriorTipo=tipo)
            if len(ct) != 0 and ct != None:
                ct = ct.pop()
                if(ct.nuevoTipo ==  tipo and ct.anteriorTipo == tipo and (ct.miembro.observacionLlamadaLider == '' or ct.miembro.observacionLlamadaLider == None)):
                    visitantes.append(ct.miembro)
    else:
        visitantes = []
    # request.session['visitantes'] = visitantes
    if request.user.has_perm("miembros.es_administrador"):
        return HttpResponseRedirect ("/administracion/")  
    return render_to_response("Miembros/miembro.html", locals(), context_instance=RequestContext(request))


isOk = False
@user_passes_test(agregarVisitanteTest, login_url="/iniciar_sesion/")
def liderAgregarMiembro(request):
    global isOk

    accion = 'Guardar'
    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == "POST":
        form = FormularioLiderAgregarMiembro(data=request.POST)
        if form.is_valid():
            nuevoMiembro = form.save(commit = False)
            nuevoMiembro.estado = 'A'
            if nuevoMiembro.conyugue != None and nuevoMiembro.conyugue != "":
                    conyugue = Miembro.objects.get(id = nuevoMiembro.conyugue.id)
                    conyugue.conyugue = nuevoMiembro
                    conyugue.estadoCivil = 'C'
                    conyugue.save()
                    nuevoMiembro.estadoCivil = 'C'
            nuevoMiembro.save()
            CambioTipo.objects.create(miembro=nuevoMiembro, autorizacion=miembro, fecha=date.today(), anteriorTipo=TipoMiembro.objects.get(nombre__iexact="visita"), nuevoTipo=TipoMiembro.objects.get(nombre__iexact="visita"))
            ok = True
        else:
            isOk = True
            messages.error(request, "Debes llenar todos los campos")
        isOk = False
    else:
        form = FormularioLiderAgregarMiembro()
    isOk = False
    return render_to_response("Miembros/agregar_miembro.html", locals(), context_instance=RequestContext(request))

@user_passes_test(liderTest, login_url="/iniciar_sesion/")
def liderListarMiembrosGrupo(request):
    if request.method == 'POST':
        if 'transladar' in request.POST:
            request.session['seleccionados'] = request.POST.getlist('seleccionados')
            return HttpResponseRedirect('/miembro/transladar_miembros/')
        else:
            request.session['seleccionados'] = request.POST.getlist('seleccionados')
            return HttpResponseRedirect('/miembro/editar_miembros/')
        
    miembro = Miembro.objects.get(usuario = request.user)
    grupo = miembro.grupoLidera()
    if grupo:
        discipulos = miembro.discipulos()
        miembrosGrupo = grupo.miembrosGrupo()
    return render_to_response("Miembros/listar_miembros_grupo.html", locals(), context_instance=RequestContext(request))

@user_passes_test(liderTest, login_url="/iniciar_sesion/")
def liderEditarMiembros(request):
    accion = 'Guardar y editar siguiente'
    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == 'POST':
        actual = request.session['actual']
        form = FormularioLiderAgregarMiembro(data=request.POST, instance=actual)
        if form.is_valid():
            nuevoMiembro = form.save()
            nuevoMiembro.usuario.username = nuevoMiembro.email
            nuevoMiembro.usuario.save()
            if nuevoMiembro.conyugue != None and nuevoMiembro.conyugue != "":
                    conyugue = Miembro.objects.get(id = nuevoMiembro.conyugue.id)
                    conyugue.conyugue = nuevoMiembro
                    conyugue.estadoCivil = 'C'
                    conyugue.save()
                    nuevoMiembro.estadoCivil = 'C'
                    nuevoMiembro.save()
        else:
            return render_to_response("Miembros/agregar_miembro.html", locals(), context_instance=RequestContext(request))
    
    if 'seleccionados' in request.session:
        faltantes = request.session['seleccionados']
        if len(faltantes) > 0:
            miembroEditar = Miembro.objects.get(id = request.session['seleccionados'].pop())
            request.session['actual'] = miembroEditar
            form = FormularioLiderAgregarMiembro(g=miembroEditar.genero,instance=miembroEditar)        
            request.session['seleccionados'] = request.session['seleccionados']
            return render_to_response("Miembros/agregar_miembro.html", locals(), context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/miembro/listar_miembros/")
    else:
        return HttpResponseRedirect("/miembro/listar_miembros/")

@user_passes_test(liderTest, login_url="/iniciar_sesion/")
def liderTransaldarMiembro(request):
    miembro = Miembro.objects.get(usuario = request.user)
    discipulos = list(miembro.discipulos())
    if 'grupos' not in request.session:
        grupos = []
        for discipulo in discipulos:
            grupo = discipulo.grupoLidera()
            if grupo != None:
                if grupo.estado == 'A' and grupo not in grupos:
                    grupos.append(grupo)
            subdiscipulos = discipulo.discipulos()
            for subd in subdiscipulos:
                discipulos.append(subd)
        request.session['grupos'] = grupos
    else:
        grupos = request.session['grupos']
    
    if request.method == 'POST':
        getlist = request.POST.getlist('menu')
        actual = request.session['actual']
        if actual not in discipulos or Group.objects.get(name__iexact='Administrador') in miembro.usuario.groups.all():
            actual.grupo = Grupo.objects.get(id=request.POST.getlist('menu')[0])
            actual.save()
        else:
            error = 'Estas tratando de cambiar un Discipulo de Grupo, para cambiar un Discipulo de grupo contacta al Administrador'
            redireccion = '/miembro/transladar_miembros/'
            nombre = 'Transladar siguiente'
            return render_to_response("error.html", locals(), context_instance=RequestContext(request))
            
    if request.session.get('seleccionados') != None:
        faltantes = request.session['seleccionados']
        if len(faltantes) > 0:
            miembroEditar = Miembro.objects.get(id = request.session['seleccionados'].pop())
            request.session['actual'] = miembroEditar
            request.session['seleccionados'] = request.session['seleccionados']
            return render_to_response("Miembros/transladar_miembro.html", locals(), context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/miembro/listar_miembros/")
    else:
        return HttpResponseRedirect("/miembro/listar_miembros/")

@user_passes_test(miembroTest, login_url='/iniciar_sesion/')
def liderEditarPerfil(request):
    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == 'POST':
        if 'contrasena' in request.POST:
            return HttpResponseRedirect("/miembro/cambiar_contrasena/")
        elif 'aceptar' in request.POST:
            form = FormularioLiderAgregarMiembro(data=request.POST, instance=miembro)
            if form.is_valid():
                miembroEditado = form.save()
                miembroEditado.usuario.username = miembroEditado.email
                miembroEditado.usuario.save()
                if miembroEditado.conyugue != None:
                    conyugue = Miembro.objects.get(id = miembroEditado.conyugue.id)
                    conyugue.conyugue = miembroEditado
                    conyugue.estadoCivil = 'C'
                    conyugue.save()
                    miembroEditado.estadoCivil = 'C'
                    miembroEditado.save()
                return HttpResponseRedirect("/miembro/perfil/"+str(miembro.id))
        else:
            return HttpResponseRedirect("/miembro/")
    else:
        form = FormularioLiderAgregarMiembro(instance=miembro, g=miembro.genero, c=miembro.conyugue)
    return render_to_response("Miembros/editar_perfil.html", locals(), context_instance=RequestContext(request))

@user_passes_test(liderTest, login_url='/iniciar_sesion/')
def cambiarContrasena(request):
    miembroUsuario = request.user
    if request.method == 'POST':
        form = FormularioCambiarContrasena(data=request.POST)
        if form.is_valid():
            if(miembroUsuario.check_password(form.cleaned_data['contrasenaAnterior']) and \
               form.cleaned_data['contrasenaNueva'] == form.cleaned_data['contrasenaNuevaVerificacion']):
                miembroUsuario.set_password(form.cleaned_data['contrasenaNueva'])
                miembroUsuario.save()
                return HttpResponseRedirect("/miembro/editar_perfil/")
            else:
                validacionContrasena = 'Error al tratar de cambiar la contraseña, verifique que la contraseña anterior sea correcta, y que concuerde la contraseña nueva y la verificación.'
                #return render_to_response("Miembros/cambiar_contrasena.html", locals(), context_instance=RequestContext(request))      
    else:
        form = FormularioCambiarContrasena()            
    return render_to_response("Miembros/cambiar_contrasena.html", locals(), context_instance=RequestContext(request))
        
@user_passes_test(liderTest, login_url="/iniciar_sesion/")
def liderLlamadasPendientesVisitantesGrupo(request):
    if request.method == 'POST':
        request.session['visitantesSeleccionados'] = request.POST.getlist('seleccionados')
        return HttpResponseRedirect('/miembro/registrar_llamada/lider/')
    
    miembro = Miembro.objects.get(usuario = request.user)
    grupo = miembro.grupoLidera()
    if grupo:
        visitantes = grupo.miembro_set.filter(fechaLlamadaLider = None)
#        miembrosGrupo = list(grupo.miembro_set.all())
#        tipo = TipoMiembro.objects.get(nombre__iexact = 'Visita')
#        visitantes = []
#        for mg in miembrosGrupo:        
#            ct = list(CambioTipo.objects.filter(miembro = mg).order_by('fecha'))#.filter(nuevoTipo=tipo, anteriorTipo=tipo)
#            if len(ct) != 0 and ct != None:
#                ct = ct.pop()
#                if(ct.nuevoTipo ==  tipo and ct.anteriorTipo == tipo and (ct.miembro.observacionLlamadaLider == '' or ct.miembro.observacionLlamadaLider == None)):
#                    visitantes.append(ct.miembro)
    return render_to_response("Miembros/listar_llamadas_pendientes.html", locals(), context_instance=RequestContext(request))

@user_passes_test(llamdaAgenteTest, login_url="/iniciar_sesion/")
def llamadasPendientesVisitantes(request):
    if request.method == 'POST':
        request.session['miembrosSeleccionados'] = request.POST.getlist('seleccionados')
        return HttpResponseRedirect('/miembro/registrar_llamada/agente/')
    
    miembro = Miembro.objects.get(usuario = request.user)
    miembrosPrimera = Miembro.objects.filter(fechaPrimeraLlamada=None)
    miembrosSegunda = Miembro.objects.filter(fechaSegundaLlamada=None).exclude(fechaPrimeraLlamada=None)
#    miembrosIglesia = Miembro.objects.all()
#    tipo = TipoMiembro.objects.get(nombre__iexact = 'Visita')
#    miembros = []    
#    for mg in miembrosIglesia:
#        ct = list(CambioTipo.objects.filter(miembro = mg).order_by('fecha'))#.filter(nuevoTipo=tipo, anteriorTipo=tipo)
#        if len(ct) != 0 and ct != None:
#            ct = ct.pop()
#            if ct.nuevoTipo ==  tipo and ct.anteriorTipo == tipo and \
#               (ct.miembro.observacionPrimeraLlamada == '' or ct.miembro.observacionPrimeraLlamada == None) and\
#               (ct.miembro.observacionSegundaLlamada == '' or ct.miembro.observacionSegundaLlamada == None):
#                miembros.append(ct.miembro)
    return render_to_response("Miembros/llamadas_pendientes_agente.html", locals(), context_instance=RequestContext(request))

@user_passes_test(liderTest, login_url="/iniciar_sesion/")
def liderLlamarVisitas(request):
    miembro = Miembro.objects.get(usuario = request.user)
    tipo = 'lider'
    if request.method == 'POST':
        aux = request.session['visitaActual']
        actual = Miembro.objects.get(id=aux['id'])#request.session['visitaActual']
        form = FormularioLlamadaLider(data=request.POST, instance=actual)
        if form.is_valid():
            nuevoLlamar = form.save(commit=False)
            nuevoLlamar.fechaLlamadaLider = date.today()
            nuevoLlamar.save()            
        else:
            return render_to_response("Miembros/registrar_llamada.html", locals(), context_instance=RequestContext(request))
    
    if 'visitantesSeleccionados' in request.session:
        faltantes = request.session['visitantesSeleccionados']
        if len(faltantes) > 0:
            print(request.session['visitantesSeleccionados'])
            try:
                miembroLlamar = Miembro.objects.get(id = request.session['visitantesSeleccionados'].pop())
                miembrol = {'id':str(miembroLlamar.id),
                            'nombre':str(miembroLlamar.nombre), 
                            'primerApellido':str(miembroLlamar.primerApellido),
                            'genero':str(miembroLlamar.genero),
                            'cedula':str(miembroLlamar.cedula),
                            'email':str(miembroLlamar.email),
                            'telefono':str(miembroLlamar.telefono),
                            'celular':str(miembroLlamar.celular),
                            'detalleLlamadaLider':str(miembroLlamar.detalleLlamadaLider)
                            }
                request.session['visitaActual'] = miembrol#miembroLlamar #linea que da el error
                form = FormularioLlamadaLider(instance = miembroLlamar)        
                request.session['visitantesSeleccionados'] = request.session['visitantesSeleccionados']
                return render_to_response("Miembros/registrar_llamada.html", locals(), context_instance=RequestContext(request))
            except IndexError:
                return
            except ValueError:
                return HttpResponseRedirect("/miembro/llamadas_pendientes/lider/")
        else:
            return HttpResponseRedirect("/miembro/llamadas_pendientes/lider/")
    else:
        return HttpResponseRedirect("/miembro/llamadas_pendientes/lider/") 

@user_passes_test(llamdaAgenteTest, login_url="/iniciar_sesion/")
def llamarVisitas(request):
    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == 'POST':
        actual = request.session['miembroActual']
        if actual.detallePrimeraLlamada == '' or actual.detallePrimeraLlamada == None:
            form = FormularioPrimeraLlamadaAgente(data=request.POST, instance=actual)
            llamada = 1
        elif actual.detalleSegundaLlamada == '' or actual.detalleSegundaLlamada == None:
            form = FormularioSegundaLlamadaAgente(data=request.POST, instance=actual)
            llamada = 2
            
        if form.is_valid():
            if llamada == 1:
                nuevoLlamar = form.save(commit=False)
                if nuevoLlamar.grupo is not None or nuevoLlamar.grupo !='':
                    lideres = Miembro.objects.filter(id__in = nuevoLlamar.grupo.listaLideres()).values('email')
                    receptores = ["%s" % (k['email']) for k in lideres]
                    camposMail = ['Nuevo Miembro', "Lider de la iglesia Casa del Rey,\n\n\
Se ha agregado un nuevo miembro a su G.A.R, por favor \
ingrese al sistema para registrar la llamada:\n\
http://iglesia.webfactional.com/iniciar_sesion\n\n\
Cordialmente,\n\
Admin",\
                    receptores]
                    sendMail(camposMail)
                nuevoLlamar.fechaPrimeraLlamada = date.today()
            elif llamada == 2:
                nuevoLlamar = form.save(commit=False)
                nuevoLlamar.fechaSegundaLlamada = date.today()
            nuevoLlamar.save()
        else:
            return render_to_response("Miembros/registrar_llamada.html", locals(), context_instance=RequestContext(request))
    
    if 'miembrosSeleccionados' in request.session:
        faltantes = request.session['miembrosSeleccionados']
        if len(faltantes) > 0:
            miembroLlamar = Miembro.objects.get(id = request.session['miembrosSeleccionados'].pop())
            request.session['miembroActual'] = miembroLlamar
            request.session['miembrosSeleccionados'] = request.session['miembrosSeleccionados']
            if miembroLlamar.fechaPrimeraLlamada == '' or miembroLlamar.fechaPrimeraLlamada == None:
                tipo = "primera"
                try:
                    miembroIngreso = CambioTipo.objects.get(miembro=miembroLlamar, nuevoTipo__nombre__iexact = 'visita').autorizacion
                    gMiembroIngreso = miembroIngreso.grupoLidera()
                except :
                    pass
                form = FormularioPrimeraLlamadaAgente(instance=miembroLlamar)        
                return render_to_response("Miembros/registrar_llamada.html", locals(), context_instance=RequestContext(request))
            elif miembroLlamar.fechaSegundaLlamada == '' or miembroLlamar.fechaSegundaLlamada == None:
                tipo = "segunda"
                form = FormularioSegundaLlamadaAgente(instance=miembroLlamar)
                return render_to_response("Miembros/registrar_llamada.html", locals(), context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("/miembro/llamadas_pendientes/agente/")
    else:
        return HttpResponseRedirect("/miembro/llamadas_pendientes/agente/")           
            
@user_passes_test(liderTest, login_url="/iniciar_sesion/")         
def liderPromoverVisitantesGrupo(request):
    miembro = Miembro.objects.get(usuario = request.user)    
    grupo = miembro.grupoLidera()
    if grupo:
        miembrosGrupo = list(grupo.miembro_set.all()) 
        if request.method == 'POST':        
            visitantesSeleccionados = request.POST.getlist('seleccionados')
            for visitante in visitantesSeleccionados:
                v = Miembro.objects.get(id=visitante)
                if v in miembrosGrupo:
                    CambioTipo.objects.create(miembro=v, autorizacion=miembro, fecha=date.today(), anteriorTipo=TipoMiembro.objects.get(nombre__iexact="Visita"), nuevoTipo=TipoMiembro.objects.get(nombre__iexact="Miembro"))        
            return HttpResponseRedirect('')
    
        tipo = TipoMiembro.objects.get(nombre__iexact = 'Visita')
        visitantes = []
        for mg in miembrosGrupo:
            ct = list(CambioTipo.objects.filter(miembro = mg).order_by('fecha'))#.filter(nuevoTipo=tipo, anteriorTipo=tipo)
            if len(ct) != 0 and ct != None:
                ct = ct.pop()
                if(ct.nuevoTipo ==  tipo and ct.anteriorTipo == tipo):
                    visitantes.append(ct.miembro)        
    return render_to_response("Miembros/listar_visitantes.html", locals(), context_instance=RequestContext(request))

@user_passes_test(miembroTest, login_url="/iniciar_sesion/")
def perfilMiembro(request, id):
    try:
        miembro = Miembro.objects.get(id = id)
    except:
        raise Http404
    grupoLidera = miembro.grupoLidera()
    escalafones = list(CambioEscalafon.objects.filter(miembro = miembro).order_by('fecha'))
    tipos = CambioTipo.objects.filter(miembro=miembro).order_by('-fecha')
    if len(escalafones) > 0:
        escalafon = escalafones.pop()        
    pasos = list(CumplimientoPasos.objects.filter(miembro = miembro).order_by('fecha'))    
    return render_to_response("Miembros/perfil.html", locals(), context_instance=RequestContext(request))

@user_passes_test(editarMiembroTest, login_url="/iniciar_sesion/")
def editarMiembro(request, id):
    try:
        miembroEditar = Miembro.objects.get(id=id) 
    except:
        raise Http404    
    miembro = Miembro.objects.get(usuario = request.user)
    accion = "Editar"
    if request.method == 'POST':
        if miembro.usuario.has_perm('miembros.es_administrador'):
            form = FormularioAdminAgregarMiembro(data = request.POST, instance = miembroEditar)
        else: 
            form = FormularioLiderAgregarMiembro(data=request.POST, instance=miembroEditar)
        if form.is_valid():
            nuevoMiembro = form.save()
            if nuevoMiembro.usuario != None:
                nuevoMiembro.usuario.username = nuevoMiembro.email
                nuevoMiembro.usuario.save()
            if nuevoMiembro.conyugue != None and nuevoMiembro.conyugue != '':
                    conyugue = Miembro.objects.get(id = nuevoMiembro.conyugue.id)
                    conyugue.conyugue = nuevoMiembro
                    conyugue.estadoCivil = 'C'
                    conyugue.save()
                    nuevoMiembro.estadoCivil = 'C'
                    nuevoMiembro.save()
    else:
        if miembro.usuario.has_perm('miembros.es_administrador'):
            form = FormularioAdminAgregarMiembro(g = miembroEditar.genero, instance = miembroEditar)
        else:
            form = FormularioLiderAgregarMiembro(g=miembroEditar.genero,instance=miembroEditar)    
    return render_to_response("Miembros/agregar_miembro.html", locals(), context_instance=RequestContext(request))

@user_passes_test(asignarGrupoTest, login_url="/iniciar_sesion/")
def asignarGrupo(request, id):
    try:
        miembroEditar = Miembro.objects.get(id=id)
    except:
        raise Http404    
    miembro = Miembro.objects.get(usuario = request.user)
    try:
        miembroIngreso = CambioTipo.objects.get(miembro=miembroEditar, nuevoTipo__nombre__iexact = 'visita').autorizacion
        gMiembroIngreso = miembroIngreso.grupoLidera()
    except :
        pass
    form = FormularioAsignarGrupo(instance = miembroEditar)    
    if request.method == 'POST':
        form = FormularioAsignarGrupo(data=request.POST, instance=miembroEditar)
        if form.is_valid():
            nuevoMiembro = form.save(commit=False)
            if nuevoMiembro.grupo is not None or nuevoMiembro.grupo !='':
                    mailLideres = Miembro.objects.filter(id__in=nuevoMiembro.grupo.listaLideres()).values('email')
                    receptores = ["%s" % (k['email']) for k in mailLideres]
                    camposMail = ['Nuevo Miembro', "Lider de la iglesia Casa del Rey,\n\n\
Se ha agregado un nuevo miembro a su G.A.R, por favor \
ingrese al sistema para registrar la llamada:\n\
http://iglesia.webfactional.com/iniciar_sesion\n\n\
Cordialmente,\n\
Admin",\
                    receptores] 
                    #sendMail(camposMail)
                    nuevoMiembro.fechaAsignacionGAR = date.today()
            nuevoMiembro.save()
            ok = True            
    return render_to_response("Miembros/asignar_grupo.html", locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def crearZona(request):
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        form = FormularioCrearZona(data=request.POST)
        if form.is_valid():
            nuevaZona = form.save()
            ok = True
    else:
        form = FormularioCrearZona()
    return render_to_response('Miembros/crear_zona.html', locals(), context_instance=RequestContext(request))
        
@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def editarZona(request, pk):
    accion = 'Editar'
    miembro = Miembro.objects.get(usuario=request.user)

    try:
        zona = Zona.objects.get(pk=pk)
    except Zona.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearZona(request.POST or None, instance=zona)

        if form.is_valid():
            ok = True
            form.save()

    else:
        print(zona)
        form = FormularioCrearZona(instance=zona)
        return render_to_response("Miembros/crear_zona.html", locals(), context_instance=RequestContext(request))

    return render_to_response("Miembros/crear_zona.html", locals(), context_instance=RequestContext(request))
    # return HttpResponseRedirect("/miembro/listar_zonas")

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def listarZonas(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(Zona, request.POST.getlist('seleccionados'))
    zonas = list(Zona.objects.all())
    return render_to_response('Miembros/listar_zonas.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def barriosDeZona(request, id):
    """
        Esta función permite listar los barrios que están registrados en determinada/
        zona
    """
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        zona = Zona.objects.get(id=id)
    except:
        raise Http404    
    if request.method == "POST":
        if 'editar' in request.POST:
            request.session['seleccionados'] = request.POST.getlist('seleccionados')
            request.session['zona'] = zona
            return HttpResponseRedirect('/miembro/editar_barrio/')
        if 'eliminar' in request.POST:
            okElim = eliminar(Barrio, request.POST.getlist('seleccionados'))
    barrios = list(Barrio.objects.filter(zona=zona))
    return render_to_response('Miembros/barrios.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def crearBarrio(request, id):
    """
        Esta función permite crear barrios de una zona en la base de datos
    """
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        zona = Zona.objects.get(id=id)
    except:
        raise Http404
    if request.method == "POST":
        form = FormularioCrearBarrio(data=request.POST)
        if form.is_valid():
            nuevoBarrio = Barrio.objects.create(zona=zona, nombre='')
            nuevoBarrio.save()
            form = FormularioCrearBarrio(data=request.POST, instance=nuevoBarrio)
            nuevoBarrio = form.save()
            ok = True
    else:
        form = FormularioCrearBarrio()
    return render_to_response('Miembros/crear_barrio.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def editarBarrio(request):
    accion = 'Editar'
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        barrio = request.session['actual']
        zona = request.session['zona']
        form = FormularioCrearZona(data=request.POST, instance=barrio)
        if form.is_valid():
            nuevoBarrio = form.save()
            ok = True
    
    if 'seleccionados' in request.session:
        faltantes = request.session['seleccionados']
        if len(faltantes) > 0:
            barrio = Barrio.objects.get(id = request.session['seleccionados'].pop())
            request.session['actual'] = barrio
            form = FormularioCrearBarrio(instance=barrio)
            request.session['seleccionados'] = request.session['seleccionados']
            return render_to_response("Miembros/crear_barrio.html", locals(), context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/miembro/barrios/'+str(zona.id))
    else:
        return HttpResponseRedirect('/miembro/barrios/'+str(zona.id))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def agregarPasoMiembro(request):
    """
        Esta función sirve para agregar un paso a la lista de pasos que puede cumplir/
        un miembro
    """
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)    
    if request.method == "POST":
        form = FormularioPasos(data=request.POST)
        if form.is_valid():
            nuevoPaso = form.save()
            ok = True
    else:
        form = FormularioPasos()    
    return render_to_response('Miembros/agregar_paso.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def  listarPasos(request):
    """
        Esta función sirve para listar los pasos con que cuenta la iglesia
    """
    miembro = Miembro.objects.get(usuario=request.user)    
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(Pasos, request.POST.getlist('seleccionados'))
    pasos = Pasos.objects.all().order_by("prioridad")
    return render_to_response('Miembros/listar_pasos.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def editarPaso(request, pk):
    accion = 'Editar'

    try:
        paso = Pasos.objects.get(pk=pk)
    except Pasos.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioPasos(request.POST or None, instance=paso)

        if form.is_valid():
            ok = True
            form.save()

    else:
        form = FormularioPasos(instance=paso)
        return render_to_response("Miembros/agregar_paso.html",locals(),context_instance=RequestContext(request))

    # return HttpResponseRedirect("/miembro/listar_pasos/")
    return render_to_response("Miembros/agregar_paso.html",locals(),context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def listarEscalafones(request):
    """
        Muestra la lista de escalafones ya creados ordenado por el número de/
        células
    """

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            okElim = eliminar(Escalafon, request.POST.getlist('seleccionados'))

    escalafones = list(Escalafon.objects.all().order_by('celulas'))
    return render_to_response('Miembros/listar_escalafones.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def crearEscalafon(request):
    """
        Crea Escalafones con sus respectivos campos
    """
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        form = FormularioCrearEscalafon(data=request.POST)
        if form.is_valid():
            nuevoEscalafon = form.save()
            ok = True
    else:
        form = FormularioCrearEscalafon()
    return render_to_response('Miembros/crear_escalafon.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def editarEscalafon(request, pk):
    accion = 'Editar'

    try:
        escalafon = Escalafon.objects.get(pk=pk)
    except Escalafon.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearEscalafon(request.POST or None, instance=escalafon)

        if form.is_valid():
            form.save()

    else:
        form = FormularioCrearEscalafon(instance=escalafon)
        return render_to_response("Miembros/crear_escalafon.html",locals(),context_instance=RequestContext(request))

    # return HttpResponseRedirect("/miembro/listar_escalafones/")
    return render_to_response("Miembros/crear_escalafon.html",locals(),context_instance=RequestContext(request))

    
@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def promoverMiembroEscalafon(request):
    """Promueve un miembro de escalafon siempre y cuando este cumpla con los requesitos para el cambio."""

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        form = FormularioPromoverEscalafon(data=request.POST)
        if form.is_valid():
            nuevoCambioEscalafon = form.save(commit=False)
            miembroEditar = nuevoCambioEscalafon.miembro
            print(miembroEditar)
            if calcularCelulas(miembroEditar) >= nuevoCambioEscalafon.escalafon.celulas:
                nuevoCambioEscalafon.save()
                ok = True
            else:
                messages.error(request,"El miembro %s no cumple con los requisitos para el cambio." % (str(miembroEditar)))
    else:
        form = FormularioPromoverEscalafon()
    return render_to_response('Miembros/promover_escalafon.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def crearTipoMiembro(request):
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        form = FormularioCrearTipoMiembro(data=request.POST)
        if form.is_valid():
            nuevoTipoMiembro = form.save()
            ok = True
    else:
        form = FormularioCrearTipoMiembro()
    return render_to_response('Miembros/crear_tipo_miembro.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def listarTipoMiembro(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        if 'editar' in request.POST:
            request.session['seleccionados'] = request.POST.getlist('seleccionados')
            return HttpResponseRedirect('/miembro/editar_tipo_miembro/')
        if 'eliminar' in request.POST:
            okElim = eliminar(TipoMiembro, request.POST.getlist('seleccionados'))   
    tipos = list(TipoMiembro.objects.all().order_by('nombre'))
    return render_to_response('Miembros/listar_tipo_miembro.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def editarTipoMiembro(request, pk):
    accion = 'Editar'

    try:
        tipo = TipoMiembro.objects.get(pk=pk)
    except TipoMiembro.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearTipoMiembro(request.POST or None, instance=tipo)

        if form.is_valid():
            ok = True
            form.save()

    else:
        form = FormularioCrearTipoMiembro(instance=tipo)
        return render_to_response("Miembros/crear_tipo_miembro.html", locals(), context_instance=RequestContext(request))

    # return HttpResponseRedirect("/miembro/listar_tipo_miembro/")
    return render_to_response("Miembros/crear_tipo_miembro.html", locals(), context_instance=RequestContext(request))

    
@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def cambiarMiembroDeTipoMiembro(request, id):
    miembro = Miembro.objects.get(usuario=request.user)    
    try:
        miembroCambio = Miembro.objects.get(id=id)
    except:
        raise Http404
    try:
        anterior = CambioTipo.objects.filter(miembro=miembroCambio).order_by('-fecha')[0].nuevoTipo 
    except:
        anterior = TipoMiembro.objects.get(nombre__iexact="visita")        
    
    if request.method == "POST":        
        form = FormularioCambioTipoMiembro(data=request.POST)
        if form.is_valid():
            nuevoCambioTipo = form.save(commit=False)
            nuevoCambioTipo.fecha = date.today()
            nuevoCambioTipo.autorizacion = miembro
            nuevoCambioTipo.miembro = miembroCambio
            nuevoCambioTipo.anteriorTipo = anterior
            nuevoCambioTipo.save()
            ok = True

            if (nuevoCambioTipo.nuevoTipo.nombre.lower() == "lider" or nuevoCambioTipo.nuevoTipo.nombre.lower() == "agente" or  \
                nuevoCambioTipo.nuevoTipo.nombre.lower() == "maestro" or nuevoCambioTipo.nuevoTipo.nombre.lower() == "receptor" or \
                nuevoCambioTipo.nuevoTipo.nombre.lower() == "administrador" or nuevoCambioTipo.nuevoTipo.nombre.lower() == "pastor"):

                if miembroCambio.usuario == None or miembroCambio.usuario == '':
                    request.session['tipo'] = nuevoCambioTipo.nuevoTipo.nombre
                    return HttpResponseRedirect('/miembro/asignar_usuario/'+str(miembroCambio.id)+'/')
                else:
                    if nuevoCambioTipo.nuevoTipo.nombre.lower() == "lider":
                        miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Lider'))
                    if nuevoCambioTipo.nuevoTipo.nombre.lower() == "agente":
                        miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Agente'))
                    if nuevoCambioTipo.nuevoTipo.nombre.lower() == "maestro":
                        miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Maestro'))
                    if nuevoCambioTipo.nuevoTipo.nombre.lower() == "receptor":
                        miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Receptor'))
                    if nuevoCambioTipo.nuevoTipo.nombre.lower() == "administrador":
                        miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Administrador'))
                    if nuevoCambioTipo.nuevoTipo.nombre.lower() == "pastor":
                        miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Pastor'))
    else:
        form = FormularioCambioTipoMiembro(idm = int(id))    
    return render_to_response('Miembros/asignar_tipo_miembro.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def crearUsuarioMimembro(request, id):
    try:
        miembroCambio = Miembro.objects.get(id=id)
    except:
        raise Http404 
    
    if request.method == "POST":
        form = FormularioAsignarUsuario(data=request.POST)
        if form.is_valid() and form.cleaned_data['contrasena'] == form.cleaned_data['contrasenaVerificacion']:
            nuevoUsuario = User()
            if form.cleaned_data['email'] != miembroCambio.email:
                miembroCambio.correo = form.cleaned_data['email']    
            nuevoUsuario.username = form.cleaned_data['email']
            nuevoUsuario.set_password(form.cleaned_data['contrasena'])
            nuevoUsuario.save()
            miembroCambio.usuario = nuevoUsuario
            miembroCambio.save()
            if request.session['tipo'].lower() == "lider":
                miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Lider'))
            if request.session['tipo'].lower() == "agente": 
                miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Agente'))
            if request.session['tipo'].lower() == "maestro": 
                miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Maestro'))
            if request.session['tipo'].lower() == "receptor": 
                miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Receptor'))
            if request.session['tipo'].lower() == "administrador":
                miembroCambio.usuario.groups.add(Group.objects.get(name__iexact='Administrador'))
        return HttpResponseRedirect('/miembro/perfil/'+str(miembroCambio.id)+'/')
    else:
        form = FormularioAsignarUsuario()
    form.email = miembroCambio.email        
    return render_to_response('Miembros/asignar_usuario.html', locals(), context_instance=RequestContext(request))
        
@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def graduarAlumno(request):
    miembro = Miembro.objects.get(usuario = request.user)

    if request.method == 'POST':
        form = FormularioCumplimientoPasosMiembro(data = request.POST)
        if form.is_valid():
            estudianteGraduado = form.save(commit = False)
            estudianteGraduado.paso = Pasos.objects.get(nombre = "lanzamiento")
            try:
                estudiante = Matricula.objects.get(estudiante = estudianteGraduado.miembro)
            except:
                raise Http404
            modulos = list(estudiante.modulos.all())
            modulosCurso = estudiante.curso.modulos.all()
            if len(modulos) == len(modulosCurso) and estudiante.notaDefinitiva >= 3:
                estudianteGraduado.fecha = datetime.datetime.now()
                estudianteGraduado.save()
                ok = True
                puedeVer = True
            else:
                ok = False
                puedeVer = False
    else:
        puedeVer=True
        form = FormularioCumplimientoPasosMiembro()
    return render_to_response('Miembros/graduar_estudiante.html', locals(), context_instance=RequestContext(request))    
    
@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def eliminarCambioTipoMiembro(request, id):
    """
        El cambio que se va a eliminar se guarda en la var cambio y si esta es un/
        tipo de cambio aceptable, es eliminado. En caso de que el usuario no cuente/
        con ningún otro tipo de miembro luego de eliminar el cambio. El usuario será/
        eliminado y no podrá loguearse en el sistema.
    """
    miembro = Miembro.objects.get(usuario=request.user)    
    try:
        cambio = CambioTipo.objects.get(id=id)
    except:
        raise Http404
         
    if cambio.nuevoTipo.nombre.lower() == "lider": 
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Lider'))
    if cambio.nuevoTipo.nombre.lower() == "agente": 
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Agente'))
    if cambio.nuevoTipo.nombre.lower() == "maestro": 
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Maestro'))
    if cambio.nuevoTipo.nombre.lower() == "receptor": 
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Receptor'))
    if cambio.nuevoTipo.nombre.lower() == "administrador": 
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Administrador'))
    if cambio.nuevoTipo.nombre.lower() == "pastor":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Pastor'))
            
    try:
        if len(cambio.miembro.usuario.groups.all()) == 0:
            cambio.miembro.usuario = None
            cambio.miembro.save()
            cambio.miembro.usuario.delete()
    except:
        pass
    cambio.delete() 
    return HttpResponseRedirect('/miembro/perfil/'+str(cambio.miembro.id))
    
def calcularCelulas(miembro):
    celulas = 0
    discipulos = list(miembro.discipulos())
    for d in discipulos:
        if d.grupoLidera():
            celulas += 1
            subdiscipulos = d.discipulos()
            for s in subdiscipulos: 
                discipulos.append(s)        
    return celulas

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def administracion(request):
    miembro = Miembro.objects.get(usuario=request.user)
    totalGrupos = Grupo.objects.all().count()
    totalGruposA = Grupo.objects.filter(estado = 'A').count()
    totalGruposI = Grupo.objects.filter(estado = 'I').count()
    totalMiembros = Miembro.objects.all().count()
    totalMiembrosA = Miembro.objects.filter(estado = 'A').count()
    totalMiembrosR = Miembro.objects.filter(estado = 'R').count()
    totalMiembrosI = Miembro.objects.filter(estado = 'I').count()
    totalLideres = CambioTipo.objects.filter(nuevoTipo = TipoMiembro.objects.get(nombre__iexact="Lider")).count()
    totalMaestros = CambioTipo.objects.filter(nuevoTipo = TipoMiembro.objects.get(nombre__iexact="Maestro")).count()
    totalCursos = Curso.objects.all().count()
    totalCursosA = Curso.objects.filter(estado='A').count()
    totalCursosC = Curso.objects.filter(estado='C').count()
    # visitantes = request.session['visitantes']
    return render_to_response('Miembros/administracion.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def AgregarDetalleLlamada(request):
    miembro = Miembro.objects.get(usuario=request.user)
    accion = 'Crear'
    if request.method == 'POST':
        form = FormularioDetalleLlamada(data = request.POST)
        if form.is_valid():
            NuevoDetalleLlamada = form.save()
            ok = True
    else:
        form = FormularioDetalleLlamada()
    return render_to_response('Miembros/agregar_detalle_llamada.html', locals(), context_instance=RequestContext(request))    

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def listarDetallesLlamada(request):
    miembro = Miembro.objects.get(usuario=request.user)  

    if request.method == "POST":

        if 'eliminar' in request.POST:
            print(request.POST.getlist('seleccionados'))
            okElim = eliminar(DetalleLlamada, request.POST.getlist('seleccionados'))

    detallesLlamada = list(DetalleLlamada.objects.all())

    return render_to_response('Miembros/listar_detalles_llamada.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/iniciar_sesion/")
def editarDetalleLlamada(request, pk):
    accion = 'Editar'

    try:
        detalle = DetalleLlamada.objects.get(pk=pk)
    except DetalleLlamada.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioDetalleLlamada(request.POST or None, instance=detalle)

        if form.is_valid():
            ok = True
            form.save()
    else:
        form = FormularioDetalleLlamada(instance=detalle)
        return render_to_response("Miembros/agregar_detalle_llamada.html", locals(), context_instance=RequestContext(request))

    return render_to_response("Miembros/agregar_detalle_llamada.html", locals(), context_instance=RequestContext(request))


@user_passes_test(cumplimientoPasosTest, login_url="/iniciar_sesion/")
def cumplimientoPasos(request):
    """Permite a un Administrador o a un Agente registrar los cumplimientos de los pasos de los miembros. Una vez seleccionado un paso,
        se muestran los miembros que pueden realizar dicho paso y los que lo hayan realizado. La condición para que un miembro pueda
        realizar un paso es que haya realizado todos los pasos con una prioridad menor al escogido."""
        
    if request.method == 'POST':
        if 'verMiembros' in request.POST or 'promoverPaso' in request.POST:           
            try:
                pasoE = Pasos.objects.get(id = request.POST.getlist('menuPasos')[0])
                numPasos = Pasos.objects.filter(prioridad__lt = pasoE.prioridad).count()
                
                if 'promoverPaso' in request.POST:
                    miembros = Miembro.objects.exclude(pasos__prioridad__gt = pasoE.prioridad).annotate(nPasos = Count('pasos')).filter(nPasos__gte = numPasos).order_by('nombre')
                    seleccionados = request.POST.getlist('seleccionados')
                    for m in miembros:
                        if str(m.id) in seleccionados:
                            if not m.pasos.filter(id = pasoE.id).exists():
                                c = CumplimientoPasos.objects.create(miembro = m, paso = pasoE, fecha = datetime.datetime.now())
                                ok = True
                        else:
                            if m.pasos.filter(id = pasoE.id).exists():
                                CumplimientoPasos.objects.get(miembro = m, paso = pasoE).delete()
                                ok = True
                
                miembros = Miembro.objects.exclude(pasos__prioridad__gt = pasoE.prioridad).annotate(nPasos = Count('pasos')).filter(nPasos__gte = numPasos).order_by('nombre')
                for m in miembros:
                    if m.pasos.filter(id = pasoE.id).exists():
                        m.cumplio = True
                    else:
                        m.cumplio = False
            except:
                raise Http404
    miembro = Miembro.objects.get(usuario = request.user)
    pasos = Pasos.objects.all().exclude(nombre__iexact = 'lanzamiento').order_by('prioridad', 'nombre')
    return render_to_response("Miembros/cumplimiento_pasos.html", locals(), context_instance=RequestContext(request))
    
def sendMail(camposMail):
    subject = camposMail[0]
    mensaje = camposMail[1]
    receptor = camposMail[2]
    send_mail(subject, mensaje, 'iglesia@mail.webfaction.com', receptor, fail_silently = False)