# Django Imports
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.urlresolvers import reverse

# Apps Imports
from .models import Grupo, ReunionGAR, ReunionDiscipulado, Red, AsistenciaDiscipulado, Predica
from .forms import (
    FormularioEditarGrupo, FormularioReportarReunionGrupo,
    FormularioReportarReunionDiscipulado, FormularioCrearRed, FormularioCrearGrupo,
    FormularioTransladarGrupo, FormularioCrearGrupoRaiz, FormularioCrearPredica,
    FormularioReportarReunionGrupoAdmin, FormularioReportesEnviados, FormularioEditarReunionGAR
)
from miembros.models import Miembro
from common.tests import (
    liderTest, adminTest, verGrupoTest, receptorAdminTest, PastorAdminTest,
    admin_or_director_red
)

# Python Packages
import datetime
import json
import copy


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def grupoRaiz(request):
    """Permite a un administrador crear o editar el grupo raiz de la iglesia."""

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == 'POST':
        try:
            grupoP = Grupo.objects.get(red=None)
            form = FormularioCrearGrupoRaiz(data=request.POST, instance=grupoP)
        except:
            form = FormularioCrearGrupoRaiz(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        try:
            grupoP = Grupo.objects.get(red=None)
            form = FormularioCrearGrupoRaiz(instance=grupoP, new=False)
        except:
            form = FormularioCrearGrupoRaiz()
    return render_to_response('Grupos/crear_grupo_admin.html', locals(), context_instance=RequestContext(request))


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


def obtener_fechas_semana(fecha):
    """
    Retorna las fechas de la semana de lunes a domingo a partir de una fecha
    """
    inicio_semana = fecha - datetime.timedelta(days=fecha.isoweekday() - 1)
    fin_semana = fecha + datetime.timedelta(days=7 - fecha.isoweekday())

    _fechas = []

    while inicio_semana <= fin_semana:
        _fechas.append(inicio_semana)
        inicio_semana += datetime.timedelta(days=1)

    return _fechas


def reunionDiscipuladoReportada(predica, grupo):
    reunion = grupo.reuniondiscipulado_set.filter(predica=predica)

    if reunion:
        return True
    else:
        return False


@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def reportarReunionGrupo(request):
    """
    Vista para crear el reporte de grupos en el sistema
    """

    miembro = Miembro.objects.get(usuario=request.user)
    grupo = miembro.grupoLidera()

    # se verifica que exista el grupo de el miembro en la sesion y que este, esté activo
    if grupo is not None and grupo.estado == Grupo.ACTIVO:

        # Se comentan estas lineas de código, porque no están siendo usadas en la actualidad

        # discipulos = miembro.discipulos()
        # miembrosGrupo = grupo.miembrosGrupo()
        # asistentesId = request.POST.getlist('seleccionados')

        if request.method == 'POST':
            form = FormularioReportarReunionGrupo(data=request.POST)
            if form.is_valid():
                reunion = form.save(commit=False)
                # se verifica que la reunion ya no haya sido reportada
                reportada = reunionReportada(reunion.fecha, grupo, 1)  # esta variable es enviada al template

                # si no esta reportada
                if not reportada:
                    # asigna el grupo y otros datos
                    reunion.grupo = grupo
                    reunion.digitada_por_miembro = True
                    # si no hicieron grupo, cambia la predica
                    if form.cleaned_data['no_realizo_grupo'] and not reunion.realizada:
                        reunion.predica = 'No se hizo Grupo'
                    # guarda el reporte en la base de datos
                    reunion.save()

                    messages.success(
                        request, _('Se ha Registrado el Reporte Existosamente, No olvides Llenar tu reporte Físico')
                    )
                    return redirect('reportar_reunion_grupo')
                else:
                    # envia mensaje de warning si ya fue reportada
                    messages.warning(
                        request,
                        _('Parece que ya se ha reportado una reunion esta semana, Preguntale a tu Co-Líder o Administrador')
                    )
            else:
                # si han ocurrido errores en el formulario, los envia
                messages.error(request, _('Ha ocurrido un error con el formulario, verifica los campos'))
        else:
            # carga el formulario en get
            form = FormularioReportarReunionGrupo()
    return render_to_response(
        'Grupos/reportar_reunion_grupo.html', locals(), context_instance=RequestContext(request)
    )


@user_passes_test(admin_or_director_red, login_url="/dont_have_permissions/")
def reportarReunionGrupoAdmin(request):

    if request.method == 'POST':
        form = FormularioReportarReunionGrupoAdmin(data=request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reportada = reunionReportada(reunion.fecha, reunion.grupo, 1)
            if not reportada:
                reunion.digitada_por_miembro = False
                reunion.confirmacionEntregaOfrenda = True
                if form.cleaned_data['no_realizo_grupo'] and not reunion.realizada:
                    reunion.predica = 'No se hizo Grupo'
                reunion.save()
                messages.success(
                    request,
                    _('Has reportado exitosamente la reunión de el grupo %s' % reunion.grupo.__str__())
                )
                return redirect('reportar_reunion_grupo_admin')
            else:
                messages.warning(
                    request,
                    _('Ya existe una reunión para esta semana')
                )
        else:
            messages.error(
                request,
                _('Ha ocurrido un error con el formulario, verifica los campos')
            )
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
def transladar_grupos(request, id_grupo):

    grupo = get_object_or_404(Grupo, id=id_grupo)
    lideres = Miembro.objects.filter(id__in=grupo.listaLideres())
    red = grupo.red

    if request.method == 'POST':
        form = FormularioTransladarGrupo(data=request.POST, red=red, grupo_id=id_grupo)

        if form.is_valid():
            grupo_escogido = Grupo.objects.get(id=request.POST['grupo'])
            for miembro in lideres:
                miembro.grupo = grupo_escogido
                miembro.save()
            ok = True

    else:
        form = FormularioTransladarGrupo(red=red, grupo_id=id_grupo)

    return render_to_response("Miembros/transladar_grupos.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def ver_reportes_grupo(request):
    if request.method == 'POST' or (
        'post' in request.session and len(request.session['post']) > 1 and request.session.get('valid_post', False)
       ):
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
        valid_post = request.session.get('valid_post', False)

        if 'reportar' in request.POST:
            form_reporte = FormularioReportarReunionGrupoAdmin(data=request.POST)

            if form_reporte.is_valid():
                reunion = form_reporte.save(commit=False)
                reportada = reunionReportada(reunion.fecha, reunion.grupo, 1)

                if reportada:
                    messages.warning(request, "El Grupo ya cuenta con un reporte en esa semana")
                    form_reporte.add_error('fecha', 'Ya hay un reporte en esta semana')
                    click = True
                    if data_from_session is not None:
                        request.POST.update(data_from_session)
                        request.session['post'] = request.session['post']
                        # request.session['post'] = request.POST
                else:
                    reunion.digitada_por_miembro = False
                    reunion.confirmacionEntregaOfrenda = True
                    if form_reporte.cleaned_data['no_realizo_grupo'] and not reunion.realizada:
                        reunion.predica = 'No se hizo Grupo'
                    reunion.save()
                    messages.success(request, "Se Ha Reportado el Sobre Correctamente")
                    # request.session['post'] = request.POST
                    if data_from_session is not None:
                        request.POST.update(data_from_session)
                        request.session['post'] = request.session['post']
                        # request.session['post'] = request.POST
                        request.session['valid_post'] = True
                    return redirect('reportes_grupo')
            else:
                if data_from_session is not None:
                    request.POST.update(data_from_session)
                    request.session['post'] = request.session['post']
                    # request.session['post'] = request.POST
                if settings.DEBUG:
                    print(form_reporte.errors)
                click = True

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
                    request.session['post'] = request.session['post']
                    # request.session['post'] = request.POST
                    request.session['valid_post'] = True
                return redirect('reportes_grupo')

        form = FormularioReportesEnviados(data=request.POST or data_from_session)

        if form.is_valid():
            grupo = form.cleaned_data['grupo']  # get_object_or_404(Grupo, id=request.POST['grupo'])
            fecha_inicial = form.cleaned_data['fechai']
            fecha_final = form.cleaned_data['fechaf']
            # se escribe la sesion con los datos de el POST
            request.session['post'] = {
                'grupo': form.cleaned_data['grupo'].id,
                'fechai': request.POST.get('fechai') or data_from_session['fechai'],
                'fechaf': request.POST.get('fechaf') or data_from_session['fechaf']
            }
            # request.session['valid_post'] = False
            request.session.pop('valid_post', None)
            fecha_final += datetime.timedelta(days=1)
            reuniones = grupo.reuniongar_set.filter(
                fecha__range=(fecha_inicial, fecha_final)
            ).order_by('-fecha')
            if len(reuniones) == 0:
                vacio = True

    else:
        form = FormularioReportesEnviados()
        form_reporte = FormularioReportarReunionGrupoAdmin()
        request.session.pop('valid_post', None)

    return render_to_response("Grupos/ver_reportes_grupo.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def editar_runion_grupo(request, pk):
    """
    Funcion para editar una reunion de Grupo GAR
    """
    reunion = get_object_or_404(ReunionGAR, pk=pk)
    fecha_anterior = copy.deepcopy(reunion.fecha)

    # se sobreescriben las variables
    request.session['post'] = request.session.pop('post', None)

    if request.method == 'POST':
        form = FormularioEditarReunionGAR(data=request.POST, instance=reunion)

        if form.is_valid():
            reunion_formulario = form.save(commit=False)

            if reunion_formulario.fecha not in obtener_fechas_semana(fecha_anterior):
                reportada = reunionReportada(reunion_formulario.fecha, reunion_formulario.grupo, 1)

                if reportada:
                    messages.warning(
                        request,
                        _('Ya hay una reunion reportada en esta semana, verifica la fecha')
                    )
                    form.add_error('fecha', _('Fecha concuerda con otro reporte de reunion'))
                else:
                    # se envia que puede ir a la pagina de vista de reportes
                    request.session['valid_post'] = True
                    if form.cleaned_data['no_realizo_grupo'] and not reunion.realizada:
                        reunion.predica = 'No se hizo Grupo'
                    reunion_formulario.save()
                    messages.success(
                        request,
                        _('Se ha editado la reunion exitosamente. \
                        <a href="%(link)s" class="alert-link">Volver a reuniones.</a>' % {'link': reverse('reportes_grupo')})
                    )
            else:
                # se envia que puede ir a la pagina de vista de reportes
                request.session['valid_post'] = True
                if form.cleaned_data['no_realizo_grupo'] and not reunion.realizada:
                    reunion.predica = 'No se hizo Grupo'
                reunion_formulario.save()
                messages.success(
                    request,
                    _('Se ha editado la reunion exitosamente. \
                    <a href="%(link)s" class="alert-link">Volver a reuniones.</a>' % {'link': reverse('reportes_grupo')})
                )
        else:
            messages.error(request, _('Ha ocurrido un error al enviar el formulario, verifica los campos'))

    else:
        form = FormularioEditarReunionGAR(instance=reunion)

    return render_to_response("Grupos/editar_reunion_grupo.html", locals(), context_instance=RequestContext(request))
