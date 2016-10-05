# Django Imports
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template.context import RequestContext
from django.views.generic import TemplateView, CreateView

# Third-Party App Imports
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin, PermissionRequiredMixin

# Apps Imports
from common.decorators import permisos_requeridos
from .models import Grupo, ReunionGAR, ReunionDiscipulado, Red, AsistenciaDiscipulado, Predica
from .forms import (
    FormularioEditarGrupo, FormularioReportarReunionGrupo,
    FormularioReportarReunionDiscipulado, FormularioCrearRed, FormularioCrearGrupo,
    FormularioTransladarGrupo, FormularioCrearPredica,
    FormularioReportarReunionGrupoAdmin, FormularioReportesEnviados, FormularioEditarReunionGAR,
    GrupoRaizForm, NuevoGrupoForm, TransladarGrupoForm
)
from miembros.models import Miembro
from common.groups_tests import (
    liderTest, adminTest, verGrupoTest, receptorAdminTest, PastorAdminTest, admin_or_director_red
)

# Python Packages
import datetime
import json


@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def editarHorarioReunionGrupo(request, pk=None):
    g = True
    miembro = Miembro.objects.get(usuario=request.user)
    mismo = True
    # grupo.miembro_set.all()
    if pk:
        try:
            miembro = Miembro.objects.get(id=pk)
            mismo = False
            if Miembro.objects.get(usuario=request.user).id == miembro.id:
                mismo = True
        except Miembro.DoesNotExist:
            raise Http404

    grupo = miembro.grupoLidera()
    if mismo:
        puede_editar = True
    if grupo is None:
        puede_editar = False
        grupo = miembro.grupo
        no_lider = True
    if grupo is not None:
        miembros = grupo.miembrosGrupo()
        lideres = Miembro.objects.filter(id__in=grupo.listaLideres())
    else:
        miembros = None
        lideres = None

    if request.method == 'POST':
        form = FormularioEditarGrupo(data=request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            ok = True
            ms = "El Grupo %s Fue Editado Correctamente" % grupo.nombre.upper()
            if mismo:
                ms = "Has Editado Tú Grupo Correctamente"
        else:
            ms = "Ocurrió un Error, Por Favor Verifica El Formulario"
    else:
        form = FormularioEditarGrupo(instance=grupo)

    return render_to_response('Grupos/editar_grupo.html', locals(), context_instance=RequestContext(request))


def reunionReportada(fecha, grupo, tipo):
    ini_semana = fecha - datetime.timedelta(days=fecha.isoweekday() - 1)
    fin_semana = fecha + datetime.timedelta(days=7 - fecha.isoweekday())

    if tipo == 1:  # GAR
        reunion = grupo.reuniongar_set.filter(fecha__gte=ini_semana, fecha__lte=fin_semana)
    else:  # DISCIPULADO
        reunion = grupo.reuniondiscipulado_set.filter(fecha__gte=ini_semana, fecha__lte=fin_semana)

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
    miembro = Miembro.objects.get(usuario=request.user)
    grupo = miembro.grupoLidera()
    if grupo and grupo.estado == 'A':
        discipulos = miembro.discipulos()
        miembrosGrupo = grupo.miembrosGrupo()
        asistentesId = request.POST.getlist('seleccionados')
        if request.method == 'POST':
            form = FormularioReportarReunionGrupo(data=request.POST)
            if form.is_valid():
                r = form.save(commit=False)
                if not reunionReportada(r.fecha, grupo, 1):
                    r.grupo = grupo
                    r.digitada_por_miembro = True
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


@user_passes_test(admin_or_director_red, login_url="/dont_have_permissions/")
def reportarReunionGrupoAdmin(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == 'POST':
        form = FormularioReportarReunionGrupoAdmin(data=request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            if not reunionReportada(reporte.fecha, reporte.grupo, 1):
                reporte.digitada_por_miembro = False
                reporte.save()
                ok = True
            else:
                ya_reportada = True
    else:
        init = request.GET.get('grupo', None)
        initial = {'grupo': init}
        form = FormularioReportarReunionGrupoAdmin(initial=initial)
    return render_to_response('Grupos/reportar_reunion_grupo_admin.html', locals(), context_instance=RequestContext(request))


@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def reportarReunionDiscipulado(request):
    miembro = Miembro.objects.get(usuario=request.user)
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
                            am = AsistenciaDiscipulado.objects.create(miembro=m, reunion=r, asistencia=True)
                        else:
                            am = AsistenciaDiscipulado.objects.create(miembro=m, reunion=r, asistencia=False)
                        am.save()
                    ok = True
                else:
                    ya_reportada = True
        else:
            form = FormularioReportarReunionDiscipulado(miembro=miembro)
    return render_to_response('Grupos/reportar_reunion_discipulado.html', locals(), context_instance=RequestContext(request))


@user_passes_test(receptorAdminTest, login_url="/dont_have_permissions/")
def registrarPagoGrupo(request, id):
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        miembroRegistrar = Miembro.objects.get(id=int(id))
    except:
        raise Http404

    if request.method == "POST":
        seleccionados = request.POST.getlist('seleccionados')
        for seleccionado in seleccionados:
            try:
                reunion = ReunionGAR.objects.get(id=seleccionado)
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
        mensaje = 'El miembro %s %s no tiene ningun grupo asignado.' % \
            (miembroRegistrar.nombre.capitalize(), miembroRegistrar.primerApellido.capitalize())
    ofrendasPendientesGar = ReunionGAR.objects.filter(grupo=grupoLidera, confirmacionEntregaOfrenda=False)
    return render_to_response("Grupos/registrar_pago_gar.html", locals(), context_instance=RequestContext(request))


@user_passes_test(receptorAdminTest, login_url="/dont_have_permissions/")
def registrarPagoDiscipulado(request, id):

    miembro = Miembro.objects.get(usuario=request.user)
    try:
        miembroRegistrar = Miembro.objects.get(id=int(id))
    except:
        raise Http404

    if request.method == "POST":
        seleccionados = request.POST.getlist('seleccionados')
        for seleccionado in seleccionados:
            try:
                reunion = ReunionDiscipulado.objects.get(id=seleccionado)
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
        mensaje = 'El miembro %s %s no tiene ningun grupo asignado.' % \
            (miembroRegistrar.nombre.capitalize(), miembroRegistrar.primerApellido.capitalize())
    ofrendasPendientesDiscipulado = ReunionDiscipulado.objects.filter(grupo=grupoLidera,
                                                                      confirmacionEntregaOfrenda=False)
    return render_to_response("Grupos/registrar_pago_discipulado.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def listarRedes(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(request, Red, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')
    redes = list(Red.objects.all())

    return render_to_response('Grupos/listar_redes.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearRed(request):
    miembro = Miembro.objects.get(usuario=request.user)
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
        return render_to_response("Grupos/crear_red.html", locals(), context_instance=RequestContext(request))

    return render_to_response("Grupos/crear_red.html", locals(), context_instance=RequestContext(request))


@user_passes_test(PastorAdminTest, login_url="/dont_have_permissions/")
def listarPredicas(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        if 'eliminar' in request.POST:
            okElim = eliminar(request, Predica, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')
    predicas = list(Predica.objects.filter(miembro__id=miembro.id))

    if Group.objects.get(name__iexact='Administrador') in request.user.groups.all():
        predicas = list(Predica.objects.all())
    return render_to_response('Grupos/listar_predicas.html', locals(), context_instance=RequestContext(request))


@user_passes_test(PastorAdminTest, login_url="/dont_have_permissions/")
def crearPredica(request):
    miembro = Miembro.objects.get(usuario=request.user)
    accion = 'Crear'
    if request.method == "POST":
        form = FormularioCrearPredica(data=request.POST, miembro=miembro)
        if form.is_valid():
            form.save()
            ok = True
    else:
        form = FormularioCrearPredica(miembro=miembro)
    return render_to_response('Grupos/crear_predica.html', locals(), context_instance=RequestContext(request))


@user_passes_test(PastorAdminTest, login_url="/dont_have_permissions/")
def editarPredica(request, pk):
    accion = 'Editar'

    miembro = Miembro.objects.get(usuario=request.user)

    try:
        predica = Predica.objects.get(pk=pk)
    except Predica.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearPredica(data=request.POST, instance=predica, miembro=miembro)
        if form.is_valid():
            ok = True
            form.save()
    else:
        form = FormularioCrearPredica(instance=predica, miembro=miembro)
        return render_to_response("Grupos/crear_predica.html", locals(), context_instance=RequestContext(request))

    return render_to_response("Grupos/crear_predica.html", locals(), context_instance=RequestContext(request))


def eliminar(request, modelo, lista):
    ok = 0  # No hay nada en la lista
    if lista:
        ok = 1  # Los borro todos
        for m in lista:
            try:
                modelo.objects.get(id=m).delete()
            except ValueError as e:
                print(e)
                pass
            except:
                ok = 2  # Hubo un error
    if ok == 1:
        messages.success(request, "Se ha eliminado correctamente")
    return ok


def listaGruposDescendientes(grupo):
    """Devuelve una lista con todos los grupos descendientes del grupo del miembro usado como parametro para ser
        usada en un choice field."""

    # grupo = miembro.grupoLidera()
    miembro = grupo.lider1
    listaG = [grupo]
    discipulos = list(miembro.discipulos())
    while len(discipulos) > 0:
        d = discipulos.pop(0)
        g = d.grupoLidera()
        if g:
            if g not in listaG:
                listaG.append(g)
            lid = Miembro.objects.filter(id__in=g.listaLideres())
            for l in lid:  # Se elimina los otros lideres de la lista de discipulos para que no se repita el grupo.
                if l in discipulos:
                    discipulos.remove(l)
        if d.discipulos():  # Se agregan los discipulos del miembro en la lista de discipulos.
            discipulos.extend(list(d.discipulos()))
    return listaG


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
        if 'eliminar' in request.POST:
            okElim = eliminar(request, Grupo, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')

    grupos = list(Grupo.objects.filter(red=red))
    for grupo in grupos:
        grupo.numero_descendientes = len(listaGruposDescendientes(grupo))

    return render_to_response('Grupos/listar_grupos.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearGrupo(request, id):
    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        red = Red.objects.get(id=id)
    except:
        raise Http404
    if request.method == "POST":
        form = FormularioCrearGrupo(data=request.POST, red=red, new=True)
        if form.is_valid():
            nuevoGrupo = form.save(commit=False)
            nuevoGrupo.red = red
            nuevoGrupo.save()
            ok = True
    else:
        form = FormularioCrearGrupo(red=red, new=True)
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
        form = FormularioCrearGrupo(data=request.POST or None, red=red, instance=grupo, new=False)

        if form.is_valid():
            nuevoGrupo = form.save()
            ok = True
    else:
        form = FormularioCrearGrupo(instance=grupo, new=False, red=red)

    return render_to_response("Grupos/crear_grupo_admin.html", locals(), context_instance=RequestContext(request))


@user_passes_test(verGrupoTest, login_url="/dont_have_permissions/")
def verGrupo(request, id):
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        grupo = Grupo.objects.get(id=id)
    except Grupo.DoesNotExist:
        raise Http404
        ok = False
    return render_to_response('Grupos/grupo.html', locals(), context_instance=RequestContext(request))


# def ConsultarReportesSinEnviar(request, sobres=False):
#     """Permite a un administrador revisar que lideres no han registrado sus reportes de reuniones de grupo
#     en un rango de fecha especificado. El administrador escoge el tipo de reunion, si la reunion es de GAR
#     (1) o discipulado (2). Luego el administrador podra enviar un mail a los lideres que no han ingresado
#     los reportes y a sus lideres."""

#     miembro = Miembro.objects.get(usuario=request.user)
#     if request.method == 'POST':
#         if 'Enviar' in request.POST:
#             if 'grupos_sin_reporte' in request.session:
#                 grupos = request.session['grupos_sin_reporte']
#                 receptores = list()
#                 for g in grupos:
#                     mailLideres = g.lideres.values('email')
#                     receptores.extend(["%s" % (k['email']) for k in mailLideres])
#                 camposMail = ['Reportes Reunion', 'mensaje', receptores]
#                 sendMail(camposMail)
#                 # mailLideres = Miembro.objects.filter(id__in = g.lideres[0].grupo.listaLideres()).values('email')
#                 # receptores = ["%s" % (k['email']) for k in mailLideres]
#                 # camposMail1 = ['Lideres Reporte Reunion', 'mensaje', receptores]

#         form = FormularioReportesSinEnviar(request.POST)
#         # Se buscan los grupos que deben reunion
#         if 'verMorosos' in request.POST:
#             if form.is_valid():
#                 tipoReunion = form.cleaned_data['reunion']
#                 fechai = form.cleaned_data['fechai']
#                 fechaf = form.cleaned_data['fechaf']
#                 grupos = []
#                 sw = True
#                 while sw:
#                     sig = fechai + datetime.timedelta(weeks=1)
#                     if tipoReunion == 1:
#                         gr = Grupo.objects.filter(estado='A').exclude(reuniongar__fecha__gte=fechai,
#                                                                       reuniongar__fecha__lt=sig)
#                     else:
#                         gr = Grupo.objects.filter(estado='A').exclude(reuniondiscipulado__fecha__gte=fechai,
#                                                                       reuniondiscipulado__fecha__lt=sig)
#                     for g in gr:
#                         try:
#                             i = grupos.index(g)
#                             if sobres:
#                                 if tipoReunion == 1:
#                                     gr = Grupo.objects.filter(
#                                         estado='A').exclude(reuniongar__fecha__gte=fechai,
#                                                             reuniongar__fecha__lt=sig,
#                                                             reuniongar__confirmacionentregaofrenda=True)
#                                 else:
#                                     gr = Grupo.objects.filter(
#                                         estado='A').exclude(reuniondiscipulado__fecha__gte=fechai,
#                                                             reuniondiscipulado__fecha__lt=sig,
#                                                             reuniondiscipulado__confirmacionentregaofrenda=True)
#                             else:
#                                 if tipoReunion == 1:
#                                     grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days=int(g.diaGAR)))
#                                 else:
#                                     grupos[i].fecha_reunion.append(fechai + datetime.timedelta(
#                                         days=int(g.diaDiscipulado)))
#                         except:
#                             if tipoReunion == 1:
#                                 g.fecha_reunion = [fechai + datetime.timedelta(days=int(g.diaGAR))]
#                             else:
#                                 g.fecha_reunion = [fechai + datetime.timedelta(days=int(g.diaDiscipulado))]
#                             g.lideres = Miembro.objects.filter(id__in=g.listaLideres())
#                             grupos.append(g)
#                     fechai = sig
#                     if sig >= fechaf:
#                         sw = False
#                 request.session['grupos_sin_reporte'] = grupos
#     else:
#         form = FormularioReportesSinEnviar()

#     return render_to_response('Grupos/morososGAR.html', locals(), context_instance=RequestContext(request))


def sendMail(camposMail):
    subject = camposMail[0]
    mensaje = camposMail[1]
    receptor = camposMail[2]
    send_mail(subject, mensaje, 'iglesia@mail.webfaction.com', receptor, fail_silently=False)


# def ConsultarSobresSinEnviar(request):
#     ConsultarReportesSinEnviar(request, True)
#     miembro = Miembro.objects.get(usuario=request.user)
#     form = FormularioReportesSinEnviar()
#     if request.method == 'POST':
#         if 'Enviar' in request.POST:
#             if 'grupos_sin_reporte' in request.session:
#                 grupos = request.session['grupos_sin_reporte']
#                 for g in grupos:
#                     mailLideres = g.lideres.values('email')
#                     receptores = ["%s" % (k['email']) for k in mailLideres]
#                     camposMail = ['Reportes Reunion', 'mensaje', receptores]
#                     print camposMail
#                     # mailLideres = Miembro.objects.filter(id__in = g.lideres[0].grupo.listaLideres()).values('email')
#                     # receptores = ["%s" % (k['email']) for k in mailLideres]
#                     # camposMail1 = ['Lideres Reporte Reunion', 'mensaje', receptores]

#         form = FormularioReportesSinEnviar(request.POST)
#         if 'verMorosos' in request.POST:
#             if form.is_valid():
#                 tipoReunion = form.cleaned_data['reunion']
#                 fechai = form.cleaned_data['fechai']
#                 fechaf = form.cleaned_data['fechaf']
#                 grupos = []
#                 sw = True
#                 while sw:
#                     sig = fechai + datetime.timedelta(weeks=1)
#                     if tipoReunion == 1:
#                         gr = Grupo.objects.filter(
#                             estado='A').exclude(reuniongar__fecha__gte=fechai,
#                                                 reuniongar__fecha__lt=sig,
#                                                 reuniongar__confirmacionentregaofrenda=True)
#                     else:
#                         gr = Grupo.objects.filter(
#                             estado='A').exclude(reuniondiscipulado__fecha__gte=fechai,
#                                                 reuniondiscipulado__fecha__lt=sig,
#                                                 reuniondiscipulado__confirmacionentregaofrenda=True)
#                     for g in gr:
#                         try:
#                             i = grupos.index(g)
#                             if tipoReunion == 1:
#                                 grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days=int(g.diaGAR)))
#                             else:
#                                grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days=int(g.diaDiscipulado)))
#                         except:
#                             pass
#                 if fechai.weekday() > 0:
#                     fechai = fechai - datetime.timedelta(days=fechai.weekday())
#                 if fechaf.weekday() < 6:
#                     if fechaf < datetime.date.today():
#                         dom = fechaf + datetime.timedelta(days=6 - fechaf.weekday())
#                         if datetime.date.today() < dom:
#                             fechaf = datetime.date.today()
#                         else:
#                             fechaf = dom
#                 sig = fechai + datetime.timedelta(weeks=1)
#                 grupos = []
#                 while sig <= fechaf:
#                     if tipoReunion == 1:
#                         g = Grupo.objects.filter(
#                             estado='A').exclude(reuniongar__fecha__gte=fechai,
#                                                 reuniongar__fecha__lt=sig,
#                                                 reuniongar__confirmacionentregaofrenda=True)
#                     else:
#                         g = Grupo.objects.filter(
#                             estado='A').exclude(reuniondiscipulado__fecha__gte=fechai,
#                                                 reuniondiscipulado__fecha__lt=sig,
#                                                 reuniondiscipulado__confirmacionentregaofrenda=True)
#                     grupos.extend(list(g))
#                     fechai = sig
#                     sig = sig + datetime.timedelta(weeks=1)

#     return render_to_response('Grupos/morososGAR.html', locals(), context_instance=RequestContext(request))


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


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def ver_reportes_grupo(request):
    if request.method == 'POST' or ('post' in request.session and len(request.session['post']) > 1):
        if 'combo' in request.POST:
            value = request.POST['value']
            querys = Q(lider1__nombre__icontains=value) | Q(lider1__primerApellido__icontains=value) | \
                Q(lider1__cedula__icontains=value) | Q(lider2__nombre__icontains=value) | \
                Q(lider2__primerApellido__icontains=value) | Q(lider2__cedula__icontains=value)
            # Importante que se puedan escoger todos los grupos y no solo los 'Activos'
            busqueda = Grupo.objects.filter(querys)[:5]
            response = [{'pk': str(s.id), 'nombre': str(s)} for s in busqueda]
            return HttpResponse(json.dumps(response), content_type='aplicattion/json')

        data_from_session = request.session.get('post', None)
        if 'reportar' in request.POST:
            form_reporte = FormularioReportarReunionGrupoAdmin(data=request.POST)

            if form_reporte.is_valid():
                reporte = form_reporte.save(commit=False)
                reporte.digitado_por_miembro = False
                if reunionReportada(reporte.fecha, reporte.grupo, 1):
                    messages.error(request, "El Grupo ya cuenta con un reporte en ese rango de fecha")
                    click = True
                    form_reporte.add_error('fecha', 'Ya hay un reporte en esta semana')
                    if data_from_session is not None:
                        request.POST.update(data_from_session)
                else:
                    reporte.save()
                    messages.success(request, "Se Ha Reportado el Sobre Correctamente")
                    # request.session['post'] = request.POST
                    if data_from_session is not None:
                        request.POST.update(data_from_session)
                    return redirect('reportes_grupo')

        else:
            form_reporte = FormularioReportarReunionGrupoAdmin()

        if 'confirmar' in request.POST:
            try:
                reunion = ReunionGAR.objects.get(id=request.POST['reporte'])
                reunion.confirmacionEntregaOfrenda = True
                reunion.save()
            except ReunionGAR.DoesNotExist:
                pass
            finally:
                if data_from_session is not None:
                    request.POST.update(data_from_session)

        form = FormularioReportesEnviados(data=request.POST or data_from_session)

        if form.is_valid():
            grupo = form.cleaned_data['grupo']  # get_object_or_404(Grupo, id=request.POST['grupo'])
            fecha_inicial = form.cleaned_data['fechai']
            fecha_final = form.cleaned_data['fechaf']
            request.session['post'] = request.POST
            fecha_final += datetime.timedelta(days=1)
            reuniones = grupo.reuniongar_set.filter(fecha__range=(fecha_inicial, fecha_final)).order_by('-fecha')
            if len(reuniones) == 0:
                vacio = True

    else:
        form = FormularioReportesEnviados()
        form_reporte = FormularioReportarReunionGrupoAdmin()

    return render_to_response("Grupos/ver_reportes_grupo.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def editar_runion_grupo(request, pk):

    reunion = get_object_or_404(ReunionGAR, pk=pk)

    if request.method == 'POST':
        form = FormularioEditarReunionGAR(data=request.POST, instance=reunion)

        if form.is_valid():
            form.save()
            ok = True
            request.session['post'] = request.session['post']

    else:
        form = FormularioEditarReunionGAR(instance=reunion)

    return render_to_response("Grupos/editar_reunion_grupo.html", locals(), context_instance=RequestContext(request))


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_lider')
def organigrama_grupos(request):
    """
    Muestra el organigrama de la red de grupos de la iglesia. Para un adminsitrador muestra toda la red, mientras que
    para un líder muestra su red.
    """

    usuario = request.user
    if usuario.has_perm('miembros.es_administrador'):
        arbol = Grupo.obtener_arbol()
    else:
        miembro = get_object_or_404(Miembro, usuario=usuario)
        arbol = Grupo.obtener_arbol(miembro.grupo_lidera)

    return render(request, 'grupos/organigrama_grupos.html', {'arbol': arbol})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def grupo_raiz(request):
    """
    Permite a un administrador crear el grupo raiz de la iglesia si aún no ha sido creado. Si ya existe lo permite
    editar.
    """

    raiz = Grupo.objects.raiz()
    if request.method == 'POST':
        form = GrupoRaizForm(instance=raiz, data=request.POST)
        if form.is_valid():
            if form.save():
                return redirect('grupos:raiz')
    else:
        form = GrupoRaizForm(instance=raiz)

    return render(request, 'grupos/grupo_raiz.html', {'form': form})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def crear_grupo(request, pk):
    """
    Permite a un administrador crear un grupo de una iglesia en la red ingresada.
    """

    red = get_object_or_404(Red, pk=pk)
    if request.method == 'POST':
        form = NuevoGrupoForm(red=red, data=request.POST)
        if form.is_valid():
            if form.save():
                return redirect('grupos:nuevo', pk)
    else:
        form = NuevoGrupoForm(red=red)

    return render(request, 'grupos/grupo_form.html', {'form': form})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def transladar(request, pk):
    """
    Permite a un administrador transladar un grupo a una nueva posición en el organigrama de grupos.
    """

    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == 'POST':
        form = TransladarGrupoForm(grupo, data=request.POST)
        if form.is_valid():
            form.transladar()
            return redirect('grupos:transladar', pk)
    else:
        form = TransladarGrupoForm(grupo)

    return render(request, 'grupos/transladar.html', {'grupo': grupo, 'form': form})
