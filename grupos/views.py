# Create your views here.
from calendar import weekday
import datetime
from xml import dom
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
import sys
from grupos.forms import FormularioEditarGrupo,\
    FormularioReportarReunionGrupo, FormularioReportarReunionDiscipulado,\
    FormularioCrearRed, FormularioCrearGrupo
from miembros.models import Miembro
from grupos.models import Grupo, AsistenciaMiembro, ReunionGAR,\
    ReunionDiscipulado, Red, AsistenciaDiscipulado
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, Http404
from academia.views import adminTest
from grupos.forms import FormularioReportesSinEnviar, FormularioCrearGrupoRaiz, FormularioCrearPredica, \
    FormularioReportarReunionGrupoAdmin
from grupos.models import Predica


def receptorTest(user):
    return  user.is_authenticated() \
            and Group.objects.get(name__iexact='Receptor') in user.groups.all()

def liderTest(user):
    return  user.is_authenticated() \
            and Group.objects.get(name__iexact='Lider') in user.groups.all()

def adminTest(user):
    return  user.is_authenticated() \
            and Group.objects.get(name__iexact='Administrador') in user.groups.all()

def verGrupoTest(user):
    return  user.is_authenticated()\
    and (Group.objects.get(name__iexact='Lider') in user.groups.all()\
         or Group.objects.get(name__iexact='Administrador') in user.groups.all())

def receptorAdminTest(user):
    return  user.is_authenticated()\
    and (Group.objects.get(name__iexact='Receptor') in user.groups.all()\
         or Group.objects.get(name__iexact='Administrador') in user.groups.all())

def PastorAdminTest(user):
    return user.is_authenticated()\
    and (Group.objects.get(name__iexact='Pastor') in user.groups.all()\
         or Group.objects.get(name__iexact='Administrador') in user.groups.all())

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def grupoRaiz(request):
    """Permite a un administrador crear o editar el grupo raiz de la iglesia."""

    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == 'POST':
        try:
            grupoP = Grupo.objects.get(red=None)
            form = FormularioCrearGrupoRaiz(data=request.POST, instance=grupoP)
        except :
            form = FormularioCrearGrupoRaiz(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        try:
            grupoP = Grupo.objects.get(red=None)
            form = FormularioCrearGrupoRaiz(instance=grupoP, new=False)
        except :
            form = FormularioCrearGrupoRaiz()
    return render_to_response('Grupos/crear_grupo_admin.html', locals(), context_instance=RequestContext(request))
            
@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def editarHorarioReunionGrupo(request):
    miembro = Miembro.objects.get(usuario = request.user)
    grupo = miembro.grupoLidera()
    # if grupo is None:
    #     raise Http404
    
    if request.method == 'POST':
        form = FormularioEditarGrupo(data=request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            ok = True
            # return HttpResponseRedirect('/miembro/')
    else:
        form = FormularioEditarGrupo(instance=grupo)    
    return render_to_response('Grupos/editar_grupo.html', locals(), context_instance=RequestContext(request))

def reunionReportada(fecha, grupo, tipo):
    ini_semana = fecha-datetime.timedelta(days = fecha.isoweekday()-1)
    fin_semana = fecha+datetime.timedelta(days = 7-fecha.isoweekday())

    if tipo==1: #GAR
        reunion = grupo.reuniongar_set.filter(fecha__gte = ini_semana, fecha__lt = fin_semana)
    else: #DISCIPULADO
        reunion = grupo.reuniondiscipulado_set.filter(fecha__gte = ini_semana, fecha__lt = fin_semana)

    if reunion:
        return True
    else:
        return False

def reunionDiscipuladoReportada(predica, grupo):
    reunion = grupo.reuniondiscipulado_set.filter(predica=predica)

    if reunion:
        return True
    else:
        return False

@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def reportarReunionGrupo(request):
    miembro = Miembro.objects.get(usuario = request.user)
    grupo = miembro.grupoLidera()
    if grupo:
        discipulos = miembro.discipulos()
        miembrosGrupo = grupo.miembrosGrupo()
        asistentesId = request.POST.getlist('seleccionados')
        if request.method == 'POST':
            form = FormularioReportarReunionGrupo(data=request.POST)
            if form.is_valid():
                r = form.save(commit=False)
                if not reunionReportada(r.fecha, grupo, 1):
                    r.grupo = grupo
                    r.save()
                    # for m in miembrosGrupo:
                    #     if unicode(m.id) in asistentesId:
                    #         am = AsistenciaMiembro.objects.create(miembro=m, reunion = r, asistencia=True)
                    #     else:
                    #         am = AsistenciaMiembro.objects.create(miembro=m, reunion = r, asistencia=False)
                    #     am.save()
                    ok = True
                else:
                    ya_reportada = True
        else:
            form = FormularioReportarReunionGrupo()    
    return render_to_response('Grupos/reportar_reunion_grupo.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def reportarReunionGrupoAdmin(request):
    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == 'POST':
        form = FormularioReportarReunionGrupoAdmin(data=request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            if not reunionReportada(r.fecha, r.grupo, 1):
                r.save()
                ok = True
            else:
                ya_reportada = True
    else:
        form = FormularioReportarReunionGrupoAdmin()
    return render_to_response('Grupos/reportar_reunion_grupo_admin.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def reportarReunionDiscipulado(request):
    miembro = Miembro.objects.get(usuario = request.user)
    grupo = miembro.grupoLidera()
    if grupo:
        discipulos = miembro.discipulos()
        asistentesId = request.POST.getlist('seleccionados')
        if request.method == 'POST':
            form = FormularioReportarReunionDiscipulado(miembro=miembro, data=request.POST)
            if form.is_valid():
                r = form.save(commit=False)
                if not reunionDiscipuladoReportada(r.predica, grupo):
                    r.grupo = grupo
                    r.save()
                    for m in discipulos:
                        if m.id in asistentesId:
                            am = AsistenciaDiscipulado.objects.create(miembro=m, reunion = r, asistencia=True)
                        else:
                            am = AsistenciaDiscipulado.objects.create(miembro=m, reunion = r, asistencia=False)
                        am.save()
                    ok = True
                else:
                    ya_reportada = True
        else:
            form = FormularioReportarReunionDiscipulado(miembro=miembro)
    return render_to_response('Grupos/reportar_reunion_discipulado.html', locals(), context_instance=RequestContext(request))

@user_passes_test(receptorAdminTest, login_url="/dont_have_permissions/")
def registrarPagoGrupo(request, id):
    
    miembro = Miembro.objects.get(usuario = request.user) 
    try:
        miembroRegistrar = Miembro.objects.get(id = int(id)) 
    except:
        raise Http404
    
    if request.method == "POST":
        seleccionados = request.POST.getlist('seleccionados')
        for seleccionado in seleccionados:
            try:
                reunion = ReunionGAR.objects.get(id= seleccionado)
            except ValueError:
                continue
            reunion.confirmacionEntregaOfrenda = True
            reunion.save()
            success = True
            mensaje = "Pago registrado exitosamente"
    
    grupoLidera = miembroRegistrar.grupoLidera()
    sw = True
    if grupoLidera is None:
        sw = False
        mensaje = 'El miembro %s %s no tiene ningun grupo asignado.' % (miembroRegistrar.nombre.capitalize(), miembroRegistrar.primerApellido.capitalize())
    ofrendasPendientesGar = ReunionGAR.objects.filter(grupo = grupoLidera, confirmacionEntregaOfrenda = False)
    return render_to_response("Grupos/registrar_pago_gar.html", locals(), context_instance=RequestContext(request))

@user_passes_test(receptorAdminTest, login_url="/dont_have_permissions/")
def registrarPagoDiscipulado(request, id):
    
    miembro = Miembro.objects.get(usuario = request.user) 
    try:
        miembroRegistrar = Miembro.objects.get(id = int(id)) 
    except:
        raise Http404
    
    if request.method == "POST":
        seleccionados = request.POST.getlist('seleccionados')
        for seleccionado in seleccionados:
            try:
                reunion = ReunionDiscipulado.objects.get(id= seleccionado)
            except ValueError:
                continue
            reunion.confirmacionEntregaOfrenda = True
            reunion.save()
            success = True
            mensaje = "Pago registrado exitosamente"
        # return HttpResponseRedirect('/miembro/perfil/'+str(miembro.id))
            
    grupoLidera = miembroRegistrar.grupoLidera()
    sw = True
    if grupoLidera is None:
        sw = False
        mensaje = 'El miembro %s %s no tiene ningun grupo asignado.' % (miembroRegistrar.nombre.capitalize(), miembroRegistrar.primerApellido.capitalize())
    ofrendasPendientesDiscipulado = ReunionDiscipulado.objects.filter(grupo = grupoLidera, confirmacionEntregaOfrenda=False)
    return render_to_response("Grupos/registrar_pago_discipulado.html", locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def listarRedes(request):
    miembro = Miembro.objects.get(usuario = request.user)    
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(Red, request.POST.getlist('seleccionados'))
    redes = list(Red.objects.all())

    return render_to_response('Grupos/listar_redes.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearRed(request):
    miembro = Miembro.objects.get(usuario = request.user)
    accion = 'Crear'
    if request.method == "POST":
        form = FormularioCrearRed(data=request.POST)
        if form.is_valid():
            nuevaRed = form.save()
            ok = True
    else:
        form = FormularioCrearRed()
    return render_to_response('Grupos/crear_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def editarRed(request, pk):
    accion = 'Editar'

    try:
        red = Red.objects.get(pk=pk)
    except Red.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearRed(request.POST or None, instance=red)

        if form.is_valid():
            ok = True
            form.save()

    else:
        form = FormularioCrearRed(instance=red)
        return render_to_response("Grupos/crear_red.html",locals(),context_instance=RequestContext(request))

    return render_to_response("Grupos/crear_red.html", locals(), context_instance=RequestContext(request))

@user_passes_test(PastorAdminTest, login_url="/dont_have_permissions/")
def listarPredicas(request):
    miembro = Miembro.objects.get(usuario = request.user)
    if request.method == "POST":
        if  'eliminar' in request.POST:
            okElim = eliminar(Predica, request.POST.getlist('seleccionados'))
    predicas = list(Predica.objects.filter(miembro__id = miembro.id))
    return render_to_response('Grupos/listar_predicas.html', locals(), context_instance=RequestContext(request))

@user_passes_test(PastorAdminTest, login_url="/dont_have_permissions/")
def crearPredica(request):
    miembro = Miembro.objects.get(usuario = request.user)
    accion = 'Crear'
    if request.method == "POST":
        form = FormularioCrearPredica(data=request.POST)
        if form.is_valid():
            nuevaPredica = Predica.objects.create(miembro=miembro, nombre='')
            nuevaPredica.save()
            form = FormularioCrearPredica(data=request.POST, instance=nuevaPredica)
            nuevaPredica = form.save()
            ok = True
    else:
        form = FormularioCrearPredica()
    return render_to_response('Grupos/crear_predica.html', locals(), context_instance=RequestContext(request))

@user_passes_test(PastorAdminTest, login_url="/dont_have_permissions/")
def editarPredica(request, pk):
    accion = 'Editar'

    try:
        predica = Predica.objects.get(pk=pk)
    except Predica.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearPredica(request.POST or None, instance=predica)

        if form.is_valid():
            ok = True
            form.save()
    else:
        form = FormularioCrearPredica(instance=predica)
        return render_to_response("Grupos/crear_predica.html",locals(),context_instance=RequestContext(request))

    return render_to_response("Grupos/crear_predica.html",locals(),context_instance=RequestContext(request))

    
def eliminar(modelo, lista):
    ok = 0 #No hay nada en la lista
    if lista:
        ok = 1 #Los borro todos
        for m in lista:
            try:
                modelo.objects.get(id=m).delete()
            except ValueError as e:
                print(e)
                pass
            except:
                ok = 2 #Hubo un error
    return ok
    
@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def gruposDeRed(request, id):
    miembro = Miembro.objects.get(usuario=request.user)

    try:
        red = Red.objects.get(id=id)
    except:
        raise Http404

    if request.method == "POST":
        if 'editar' in request.POST:
            request.session['seleccionados'] = request.POST.getlist('seleccionados')
            request.session['red'] = red
            return HttpResponseRedirect('/grupo/editar_grupo/')
        if  'eliminar' in request.POST:
            okElim = eliminar(Grupo, request.POST.getlist('seleccionados'))

    grupos = list(Grupo.objects.filter(red=red))

    return render_to_response('Grupos/listar_grupos.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearGrupo(request, id):
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        red = Red.objects.get(id = id)
    except:
        raise Http404
    if request.method == "POST":
        form = FormularioCrearGrupo(data=request.POST, red = id)
        if form.is_valid():
            form = FormularioCrearGrupo(data=request.POST, red = id)
            nuevoGrupo = form.save(commit=False)
            nuevoGrupo.red = red
            nuevoGrupo.save()
            ok = True
    else:
        form = FormularioCrearGrupo(red = id)
    return render_to_response('Grupos/crear_grupo_admin.html', locals(), context_instance=RequestContext(request))

@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def editarGrupo(request, pk):
    accion = 'Editar'
    miembro = Miembro.objects.get(usuario=request.user)
    
    try:
        grupo = Grupo.objects.get(pk=pk)
    except Grupo.DoesNotExist:
        raise Http404

    red = grupo.red
    if request.method == 'POST':
        form = FormularioCrearGrupo(data=request.POST or None, instance=grupo, new=False)

        if form.is_valid():
            nuevoGrupo = form.save()
            ok = True
    else:
        form = FormularioCrearGrupo(instance=grupo, new=False)

    return render_to_response("Grupos/crear_grupo_admin.html", locals(), context_instance=RequestContext(request))
    
@user_passes_test(verGrupoTest, login_url="/dont_have_permissions/")
def verGrupo(request, id):
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        grupo = Grupo.objects.get(id=id)
    except:
        ok = False
    return render_to_response('Grupos/grupo.html', locals(), context_instance=RequestContext(request))

#def ConsultarReportesSinEnviar(request, sobres=False):
#    """Permite a un administrador revisar que lideres no han registrado sus reportes de reuniones de grupo en un rango de fecha
#        especificado. El administrador escoge el tipo de reunion, si la reunion es de GAR(1) o discipulado (2). Luego el administrador
#        podra enviar un mail a los lideres que no han ingresado los reportes y a sus lideres."""
#
#    miembro = Miembro.objects.get(usuario=request.user)
#    if request.method == 'POST':
#        if 'Enviar' in request.POST:
#            if 'grupos_sin_reporte' in request.session:
#                grupos = request.session['grupos_sin_reporte']
#                receptores = list()
#                for g in grupos:
#                    mailLideres = g.lideres.values('email')
#                    receptores.extend(["%s" % (k['email']) for k in mailLideres])
#                camposMail = ['Reportes Reunion', 'mensaje', receptores]
#                sendMail(camposMail)
#                    #mailLideres = Miembro.objects.filter(id__in = g.lideres[0].grupo.listaLideres()).values('email')
#                    #receptores = ["%s" % (k['email']) for k in mailLideres]
#                    #camposMail1 = ['Lideres Reporte Reunion', 'mensaje', receptores]
#
#        form = FormularioReportesSinEnviar(request.POST)
#        #Se buscan los grupos que deben reunion
#        if 'verMorosos' in request.POST:
#            if form.is_valid():
#                tipoReunion = form.cleaned_data['reunion']
#                fechai = form.cleaned_data['fechai']
#                fechaf = form.cleaned_data['fechaf']
#                grupos = []
#                sw = True
#                while sw:
#                    sig = fechai + datetime.timedelta(weeks = 1)
#                    if tipoReunion == 1:
#                        gr = Grupo.objects.filter(estado='A').exclude(reuniongar__fecha__gte = fechai, reuniongar__fecha__lt = sig)
#                    else:
#                        gr = Grupo.objects.filter(estado='A').exclude(reuniondiscipulado__fecha__gte = fechai, reuniondiscipulado__fecha__lt = sig)
#                    for g in gr:
#                        try:
#                            i = grupos.index(g)
#                            if sobres:
#                                if tipoReunion == 1:
#                                    gr = Grupo.objects.filter(estado='A').exclude(reuniongar__fecha__gte = fechai, reuniongar__fecha__lt = sig, reuniongar__confirmacionentregaofrenda = True)
#                                else:
#                                    gr = Grupo.objects.filter(estado='A').exclude(reuniondiscipulado__fecha__gte = fechai, reuniondiscipulado__fecha__lt = sig, reuniondiscipulado__confirmacionentregaofrenda = True)
#                            else:
#                                if tipoReunion == 1:
#                                    grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days = int(g.diaGAR)))
#                                else:
#                                    grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days = int(g.diaDiscipulado)))
#                        except:
#                            if tipoReunion == 1:
#                                g.fecha_reunion = [fechai + datetime.timedelta(days = int(g.diaGAR))]
#                            else:
#                                g.fecha_reunion = [fechai + datetime.timedelta(days = int(g.diaDiscipulado))]
#                            g.lideres = Miembro.objects.filter(id__in = g.listaLideres())
#                            grupos.append(g)
#                    fechai = sig
#                    if sig >= fechaf:
#                        sw = False
#                request.session['grupos_sin_reporte'] = grupos
#    else:
#        form = FormularioReportesSinEnviar()
#
#    return render_to_response('Grupos/morososGAR.html', locals(), context_instance=RequestContext(request))

def sendMail(camposMail):
    subject = camposMail[0]
    mensaje = camposMail[1]
    receptor = camposMail[2]
    send_mail(subject, mensaje, 'iglesia@mail.webfaction.com', receptor, fail_silently = False)

#def ConsultarSobresSinEnviar(request):
#    ConsultarReportesSinEnviar(request, True)
#    miembro = Miembro.objects.get(usuario=request.user)
#    form = FormularioReportesSinEnviar()
#    if request.method == 'POST':
#        if 'Enviar' in request.POST:
#            if 'grupos_sin_reporte' in request.session:
#                grupos = request.session['grupos_sin_reporte']
#                for g in grupos:
#                    mailLideres = g.lideres.values('email')
#                    receptores = ["%s" % (k['email']) for k in mailLideres]
#                    camposMail = ['Reportes Reunion', 'mensaje', receptores]
#                    print camposMail
#                    #mailLideres = Miembro.objects.filter(id__in = g.lideres[0].grupo.listaLideres()).values('email')
#                    #receptores = ["%s" % (k['email']) for k in mailLideres]
#                    #camposMail1 = ['Lideres Reporte Reunion', 'mensaje', receptores]
#
#        form = FormularioReportesSinEnviar(request.POST)
#        if 'verMorosos' in request.POST:
#            if form.is_valid():
#                tipoReunion = form.cleaned_data['reunion']
#                fechai = form.cleaned_data['fechai']
#                fechaf = form.cleaned_data['fechaf']
#                grupos = []
#                sw = True
#                while sw:
#                    sig = fechai + datetime.timedelta(weeks = 1)
#                    if tipoReunion == 1:
#                        gr = Grupo.objects.filter(estado='A').exclude(reuniongar__fecha__gte = fechai, reuniongar__fecha__lt = sig, reuniongar__confirmacionentregaofrenda = True)
#                    else:
#                        gr = Grupo.objects.filter(estado='A').exclude(reuniondiscipulado__fecha__gte = fechai, reuniondiscipulado__fecha__lt = sig, reuniondiscipulado__confirmacionentregaofrenda = True)
#                    for g in gr:
#                        try:
#                            i = grupos.index(g)
#                            if tipoReunion == 1:
#                                grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days = int(g.diaGAR)))
#                            else:
#                                grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days = int(g.diaDiscipulado)))
#                        except:
#
#                if fechai.weekday() > 0:
#                    fechai = fechai - datetime.timedelta(days = fechai.weekday())
#                if fechaf.weekday() < 6:
#                    if fechaf < datetime.date.today():
#                        dom = fechaf + datetime.timedelta(days = 6-fechaf.weekday())
#                        if datetime.date.today() < dom:
#                            fechaf = datetime.date.today()
#                        else:
#                            fechaf = dom
#                sig = fechai + datetime.timedelta(weeks = 1)
#                grupos = []
#                while sig <= fechaf:
#                    if tipoReunion == 1:
#                        g = Grupo.objects.filter(estado='A').exclude(reuniongar__fecha__gte = fechai, reuniongar__fecha__lt = sig, reuniongar__confirmacionentregaofrenda = True)
#                    else:
#                        g = Grupo.objects.filter(estado='A').exclude(reuniondiscipulado__fecha__gte = fechai, reuniondiscipulado__fecha__lt = sig, reuniondiscipulado__confirmacionentregaofrenda = True)
#                    grupos.extend(list(g))
#                    fechai = sig
#                    sig = sig + datetime.timedelta(weeks = 1)
#
#    return render_to_response('Grupos/morososGAR.html', locals(), context_instance=RequestContext(request))

def reporteVisitasPorRed(request):
    redes = Red.objects.all()
    data = []
    for red in redes:
        grupos = Grupo.objects.filter(red=red.id)
        visRed = 0
        l = [red.nombre]
        for grupo in grupos:
            visReuniones = ReunionGAR.objects.filter(grupo=grupo.id).values('numeroVisitas')
            if len(visReuniones.values()) > 0:
                visitas = sum([int(dict['numeroVisitas']) for dict in visReuniones.values('numeroVisitas')])
                visRed = visRed + visitas
        l.append(visRed)
        data.append(l)
    return render_to_response('reportes/visitas_por_red.html', {'values': data}, context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url='/dont_have_permissions/')
def faltante_confirmar_ofrenda(request):
    grupos = ReunionGAR.objects.filter(confirmacionEntregaOfrenda=False).distinct('grupo')
    return render_to_response('Grupos/faltante_confirmar_ofrenda.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url='/dont_have_permissions/')
def faltante_confirmar_ofrenda_discipulado(request):
    grupos = ReunionDiscipulado.objects.filter(confirmacionEntregaOfrenda=False).distinct('grupo')
    return render_to_response('Grupos/faltante_confirmar_ofrenda_discipulado.html', locals(), context_instance=RequestContext(request))