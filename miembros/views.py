# Django Imports
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _

# Apps Imports
from .forms import *
from .forms import TrasladarMiembroForm, NuevoMiembroForm
from .models import Miembro, CambioTipo, TipoMiembro
from .decorators import user_is_miembro_or_empleado
from academia.models import Curso
from compras.models import Requisicion, Parametros, DetalleRequisicion
from common.decorators import permisos_requeridos
from grupos.models import Grupo, Red
from grupos.forms import FormularioEditarDiscipulado

# Third Apps
import waffle

# Python Packages
import datetime
import json
import os


def eliminar(request, modelo, lista):
    ok = 0  # No hay nada en la lista
    if lista:
        ok = 1  # Los borro todos
        for e in lista:
            try:
                if isinstance(e, str):
                    modelo.objects.get(id=int(e)).delete()
                else:
                    modelo.objects.get(id=e).delete()
            except ValueError as e:
                if settings.DEBUG:
                    print(e)
                pass
            except:
                ok = 2  # Hubo un Error
    if ok == 1:
        messages.success(request, "Se ha eliminado correctamente")
    return ok


def divorciar(miembro, conyugue, estado_civil):
    miembro.estadoCivil = estado_civil
    miembro.conyugue = None
    miembro.save()
    conyugue.estadoCivil = estado_civil
    conyugue.conyugue = None
    conyugue.save()


def autenticarUsario(request):
    siguiente = request.session.get('next', '')
    if request.user.is_authenticated():
        if request.user.has_perm("miembros.es_administrador"):
            return HttpResponseRedirect("/administracion/")
        else:
            return HttpResponseRedirect("/miembro/")
    else:
        valido = True
        if request.method == 'POST':
            nombreUsuario = request.POST.get('email', '')
            contrasena = request.POST.get('password', '')
            sig = request.POST.get('next', '')
            if siguiente:
                sig = siguiente
            usuario = auth.authenticate(email=nombreUsuario, password=contrasena)
            if usuario is not None:
                auth.login(request, usuario)
                if Group.objects.get(name__iexact='Administrador') in usuario.groups.all():
                    if sig is not None or sig != '':
                        return HttpResponseRedirect(sig)
                    return HttpResponseRedirect("/administracion/")
                else:
                    if sig is not None or sig != '':
                        return HttpResponseRedirect(sig)
                    return HttpResponseRedirect('/miembro/')
            else:
                valido = False
    return render_to_response('miembros/login.html', locals(), context_instance=RequestContext(request))


def salir(request):
    auth.logout(request)
    return HttpResponseRedirect('/iniciar_sesion')


@login_required
@user_is_miembro_or_empleado
def miembroInicio(request):
    miembro = None
    empleado = None
    try:
        miembro = Miembro.objects.get(usuario=request.user)
    except Miembro.DoesNotExist:
        empleado = request.user.empleado

    if request.user.has_perm("miembros.es_administrador"):
        return HttpResponseRedirect("/administracion/")

    if miembro:
        grupo = miembro.grupo_lidera
        if grupo:
            miembrosGrupo = grupo.miembros.all()
            tipo = TipoMiembro.objects.get(nombre__iexact='visita')
            visitantes = []
            for mg in miembrosGrupo:
                ct = CambioTipo.objects.filter(miembro=mg).order_by('id')
                if ct.exists():
                    ct = list(ct).pop()
                    if (ct.nuevoTipo == tipo and ct.anteriorTipo == tipo and (
                       ct.miembro.observacionLlamadaLider == '' or
                       ct.miembro.observacionLlamadaLider is None)
                    ):
                        visitantes.append(ct.miembro)
        else:
            visitantes = []

        discipulos = list()
        inactivos = list()
        grupos = list()

        def lid_gru(miem):
            visitas = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
            grupo = miem.grupo_lidera
            if grupo:
                return grupo.miembros.filter(id__in=visitas)
            else:
                return []

        k = Grupo.get_tree(grupo)

        discipulos = Miembro.objects.lideres().filter(grupo_lidera__in=k)
        totalLideres = len(discipulos)
        totalGrupos = len(k)  # len(grupos)
        lideresGrupo = len(lid_gru(miembro)) - 1
        if lideresGrupo == -1:
            lideresGrupo = 0
    if empleado:
        if waffle.switch_is_active('compras'):
            if empleado.requisicion_set.filter(estado=Requisicion.PROCESO).exists():
                mis_requisiciones_activas = empleado.requisicion_set.filter(estado=Requisicion.PROCESO)

            if empleado.is_compras:
                # se sacan las ulimas requisiciones
                ultimas_requisiciones = Requisicion.objects.ingresadas_compras()
                hoy = timezone.now().date()

                # se sacan las requisiciones ingresadas en el ultimo mes
                requisiciones_ingresadas_mes = Requisicion.objects.ultimo_mes().count()

                # se sacan las requisiciones que fueron atendidas por el empleado
                if requisiciones_ingresadas_mes > 0:
                    porcentage_atencion_mes = (Requisicion.objects.ultimo_mes(
                        historial__empleado=empleado
                    ).count() * 100) / requisiciones_ingresadas_mes
                else:
                    porcentage_atencion_mes = 0

                # Requisiciones en compras
                requisiciones_empleado = ultimas_requisiciones.count()

                try:
                    # porcentaje total de requisiciones en comrpas
                    porcetaje_total_en_compras = (ultimas_requisiciones.count() * 100) / Requisicion.objects.filter(
                        estado=Requisicion.PROCESO
                    ).count()
                except ZeroDivisionError:
                    porcetaje_total_en_compras = 0
            if empleado.is_jefe_administrativo:
                dias = Parametros.objects.dias()
                hoy = timezone.now().date()

                # las terminadas en este mes
                requisiciones_terminadas = Requisicion.objects.finalizadas_mes().count()

                # que han ingresado a trazabilidad
                requisiciones_faltantes_aprobar_trazabilidad = Requisicion.objects.ingresadas_administrativo().count()

                requisiciones_recientes = Requisicion.objects.ingresadas_administrativo()

                # que han ingresado a departamento
                requisiciones_faltantes_aprobar_departamento = Requisicion.objects.filter(
                    historial=None, empleado__areas__departamento__nombre__icontains='administra'
                ).count()

                requisiciones_mora = len([
                    requisicion for requisicion in Requisicion.objects.ingresadas_compras().prefetch_related(
                        'historial_set'
                    )
                    if requisicion.historial_set.last().fecha.date() + datetime.timedelta(days=dias) <= hoy
                ])

                if Requisicion.objects.filter(estado=Requisicion.PROCESO).exists():
                    porcetaje_total_en_compras = (requisiciones_faltantes_aprobar_trazabilidad * 100) /\
                        Requisicion.objects.filter(
                            estado=Requisicion.PROCESO
                        ).count()
                else:
                    porcetaje_total_en_compras = 0

            if empleado.is_jefe_financiero:
                hoy = timezone.now().date()
                requisiciones_faltantes_aprobar_departamento = Requisicion.objects.filter(
                    historial=None, empleado__areas__departamento__nombre__icontains='financi'
                ).count()

                requisiciones_faltantes_aprobar_trazabilidad = len(Requisicion.objects.ingresadas_financiero())

                requisiciones_espera = [requisicion for requisicion in Requisicion.objects.filter(
                    estado=Requisicion.PROCESO
                ) if requisicion.get_rastreo() == Requisicion.DATA_SET['espera_presupuesto']]

                salida_credito = DetalleRequisicion.objects.salida_credito_mes()['total_aprobado__sum'] or 0

                salida_efectivo = DetalleRequisicion.objects.salida_efectivo_mes()['total_aprobado__sum'] or 0

    return render_to_response("miembros/miembro.html", locals(), context_instance=RequestContext(request))


@login_required
@permisos_requeridos(
    'miembros.es_administrador', 'miembros.es_lider', 'miembros.es_agente', 'miembros.es_maestro',
    'grupos.puede_confirmar_ofrenda_discipulado', 'puede_confirmar_ofrenda_GAR'
)
def liderEditarPerfil(request, pk=None):
    p = True
    miembro = Miembro.objects.get(usuario=request.user)
    casado = False
    mismo = True
    if pk:
        try:
            miembro = Miembro.objects.get(id=pk)
            mismo = False
            if Miembro.objects.get(usuario=request.user).id == miembro.id:
                mismo = True
        except Miembro.DoesNotExist:
            raise Http404

    if miembro.estadoCivil == 'C' and miembro.conyugue is not None:
        casado = True

    foto = False
    if miembro.foto_perfil:
        rut_perfil = miembro.foto_perfil.path
        foto = True
    if request.method == 'POST':

        if 'file' in request.POST:
            dat = {}
            f = FormularioFotoPerfil(data=request.POST, files=request.FILES, instance=miembro)
            if f.is_valid():
                if miembro.foto_perfil != '' or miembro.foto_perfil is not None:
                    if foto:
                        r = settings.MEDIA_ROOT + "/media/profile_pictures/user_%s/" % miembro.id
                        if os.path.exists(rut_perfil) and os.path.isfile(rut_perfil):
                            if settings.DEBUG:
                                print("Se borra el archivo anterior")
                            os.remove(rut_perfil)
                f.save()
                ok = True
                dat['ms'] = "Foto editada Correctamente"
                dat['status'] = 'success'
                dat['ruta'] = str(miembro.foto_perfil.url)
                return HttpResponse(json.dumps(dat), content_type="application/json")
            else:
                dat['ms'] = "Foto demasiado Grande Tamaño maximo aceptado: 2000x2000"
                dat['status'] = 'danger'
                if foto:
                    dat['ruta'] = str(miembro.foto_perfil.url)
                else:
                    dat['ruta'] = settings.STATIC_URL + 'Imagenes/profile-none.jpg'
                return HttpResponse(json.dumps(dat), content_type="application/json")

        if 'contrasena' in request.POST:
            return HttpResponseRedirect("/miembro/cambiar_contrasena/")

        elif 'aceptar' in request.POST:
            if request.user.has_perm('miembros.es_administrador'):
                form = FormularioAdminAgregarMiembro(data=request.POST, files=request.FILES, instance=miembro)
                admin = True
            else:
                form = FormularioLiderAgregarMiembro(data=request.POST, files=request.FILES, instance=miembro)
            if form.is_valid():
                miembroEditado = form.save()
                if miembroEditado.usuario is not None:
                    miembroEditado.usuario.username = '{}'.format(miembroEditado.cedula)
                    miembroEditado.usuario.email = miembroEditado.email
                    miembroEditado.usuario.save()
                    miembroEditado.save()
                if miembroEditado.conyugue is not None:
                    conyugue = Miembro.objects.get(id=miembroEditado.conyugue.id)
                    conyugue.conyugue = miembroEditado
                    conyugue.estadoCivil = 'C'
                    conyugue.save()
                    miembroEditado.estadoCivil = 'C'
                    miembroEditado.save()
                if casado and miembroEditado.estadoCivil != 'C':
                    conyugue = Miembro.objects.get(conyugue=miembroEditado)
                    divorciar(miembroEditado, conyugue, miembroEditado.estadoCivil)

                ok = True
                ms = "Miembro Editado Correctamente"
                if mismo:
                    ms = "Te has Editado Correctamente"
                # return HttpResponseRedirect("/miembro/perfil/" + str(miembro.id))
            else:
                ms = "Ha Ocurrido un Error, Verifica el Formulario"
        else:
            return HttpResponseRedirect("/miembro/")
    else:
        if request.user.has_perm('miembros.es_administrador'):
            form = FormularioAdminAgregarMiembro(instance=miembro, g=miembro.genero)
            admin = True
        else:
            form = FormularioLiderAgregarMiembro(instance=miembro, g=miembro.genero, c=miembro.conyugue)
    return render_to_response("miembros/editar_perfil.html", locals(), context_instance=RequestContext(request))


@login_required
@permisos_requeridos(
    'miembros.es_administrador', 'miembros.es_lider', 'miembros.es_agente', 'miembros.es_maestro',
    'grupos.puede_confirmar_ofrenda_discipulado', 'puede_confirmar_ofrenda_GAR'
)
def cambiarContrasena(request):
    miembroUsuario = request.user
    if request.method == 'POST':
        form = FormularioCambiarContrasena(data=request.POST, request=request)
        if form.is_valid():
            if (miembroUsuario.check_password(form.cleaned_data['contrasenaAnterior']) and
               form.cleaned_data['contrasenaNueva'] == form.cleaned_data['contrasenaNuevaVerificacion']):
                miembroUsuario.set_password(form.cleaned_data['contrasenaNueva'])
                miembroUsuario.save()
                if hasattr(miembroUsuario, 'empleado') and not Miembro.objects.filter(usuario=miembroUsuario):
                    return HttpResponseRedirect("/miembro/")
                return HttpResponseRedirect("/miembro/editar_perfil/")
            else:
                validacionContrasena = """
                Error al tratar de cambiar la contraseña, verifique que la contraseña\
                anterior sea correcta, y que concuerde la contraseña nueva y la verificación.
                """
    else:
        form = FormularioCambiarContrasena(request=request)
    return render_to_response("miembros/cambiar_contrasena.html", locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.puede_editar_miembro', raise_exception=True)
def editarMiembro(request, id):
    try:
        miembroEditar = Miembro.objects.get(id=id)
    except:
        raise Http404
    miembro = Miembro.objects.get(usuario=request.user)
    accion = "Editar"
    if request.method == 'POST':
        if miembro.usuario.has_perm('miembros.es_administrador'):
            form = FormularioAdminAgregarMiembro(data=request.POST, instance=miembroEditar)
            admin = True
        else:
            form = FormularioLiderAgregarMiembro(data=request.POST, instance=miembroEditar)
            lider = True
        if form.is_valid():
            nuevoMiembro = form.save(commit=False)
            nuevoMiembro.estado = 'A'
            nuevoMiembro.save()
            if nuevoMiembro.usuario is not None:
                nuevoMiembro.usuario.username = nuevoMiembro.nombre + nuevoMiembro.primerApellido
                nuevoMiembro.usuario.email = nuevoMiembro.email
                nuevoMiembro.usuario.save()
            if nuevoMiembro.conyugue is not None and nuevoMiembro.conyugue != '':
                    conyugue = Miembro.objects.get(id=nuevoMiembro.conyugue.id)
                    conyugue.conyugue = nuevoMiembro
                    conyugue.estadoCivil = 'C'
                    conyugue.save()
                    nuevoMiembro.estadoCivil = 'C'
                    nuevoMiembro.save()
            return HttpResponseRedirect("/miembro/perfil/" + str(nuevoMiembro.id) + "/")
    else:
        if miembro.usuario.has_perm('miembros.es_administrador'):
            form = FormularioAdminAgregarMiembro(g=miembroEditar.genero, instance=miembroEditar)
            admin = True
        else:
            form = FormularioLiderAgregarMiembro(g=miembroEditar.genero, instance=miembroEditar)
            lider = True
    return render_to_response("miembros/agregar_miembro.html", locals(), context_instance=RequestContext(request))


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_agente')
def asignarGrupo(request, id):
    try:
        miembroEditar = Miembro.objects.get(id=id)
    except:
        raise Http404
    miembro = Miembro.objects.get(usuario=request.user)

    form = FormularioAsignarGrupo(instance=miembroEditar)
    if request.method == 'POST':
        form = FormularioAsignarGrupo(data=request.POST, instance=miembroEditar)
        if form.is_valid():
            nuevoMiembro = form.save(commit=False)
            if nuevoMiembro.grupo is not None or nuevoMiembro.grupo != '':
                mailLideres = nuevoMiembro.grupo.lideres.values('email')
                receptores = ["%s" % (k['email']) for k in mailLideres]
                camposMail = ['Nuevo Miembro', "Lider de la iglesia %s,\n\n\
                        Se ha agregado un nuevo miembro a su G.A.R, por favor \
                        ingrese al sistema para registrar la llamada:\n\
                        http://iglesia.webfactional.com/iniciar_sesion\n\n\
                        Cordialmente,\n\
                        Admin" % Site.objects.get_current().name, receptores]
                nuevoMiembro.fechaAsignacionGAR = datetime.date.today()
            nuevoMiembro.save()
            ok = True
    return render_to_response("miembros/asignar_grupo.html", locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
    return render_to_response('miembros/crear_zona.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
        form = FormularioCrearZona(instance=zona)
        return render_to_response("miembros/crear_zona.html", locals(), context_instance=RequestContext(request))

    return render_to_response("miembros/crear_zona.html", locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listarZonas(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(request, Zona, request.POST.getlist('seleccionados'))
            if okElim == 1:
                messages.success(request, "Se eliminaron las zonas seleccionadas")
                return HttpResponseRedirect('')
    zonas = list(Zona.objects.all())
    return render_to_response('miembros/listar_zonas.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
            okElim = eliminar(request, Barrio, request.POST.getlist('seleccionados'))
    barrios = list(Barrio.objects.filter(zona=zona))
    return render_to_response('miembros/barrios.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def crearBarrio(request, id):
    """
        Esta función permite crear barrios de una zona en la base de datos
    """
    accion = 'Crear'
    # miembro = Miembro.objects.get(usuario=request.user)
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
    return render_to_response('miembros/crear_barrio.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def editarBarrio(request, id, pk):
    accion = 'Editar'
    # miembro = Miembro.objects.get(usuario=request.user)
    try:
        zona = Zona.objects.get(id=int(id))
    except Zona.DoesNotExis:
        raise Http404
    try:
        barrio = Barrio.objects.get(pk=pk)
    except Barrio.DoesNotExist:
        raise Http404

    if request.method == "POST":
        # barrio = request.session['actual']
        form = FormularioCrearBarrio(request.POST or None, instance=barrio)
        if form.is_valid():
            nuevoBarrio = form.save()
            ok = True
        else:
            return render_to_response("miembros/crear_barrio.html", locals(), context_instance=RequestContext(request))

    else:
        form = FormularioCrearBarrio(instance=barrio)
        return render_to_response("miembros/crear_barrio.html", locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect('/miembro/barrios/' + str(zona.id))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def agregarPasoMiembro(request):
    """
    Esta función sirve para agregar un paso a la lista de pasos que puede cumplir
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
    return render_to_response('miembros/agregar_paso.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listarPasos(request):
    """
    Esta función sirve para listar los pasos con que cuenta la iglesia
    """
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(request, Pasos, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')
    pasos = Pasos.objects.all().order_by("prioridad")
    return render_to_response('miembros/listar_pasos.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
        return render_to_response("miembros/agregar_paso.html", locals(), context_instance=RequestContext(request))

    # return HttpResponseRedirect("/miembro/listar_pasos/")
    return render_to_response("miembros/agregar_paso.html", locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listarEscalafones(request):
    """
    Muestra la lista de escalafones ya creados ordenado por el número de
    células
    """

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            okElim = eliminar(request, Escalafon, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')

    escalafones = list(Escalafon.objects.all().order_by('celulas'))
    return render_to_response('miembros/listar_escalafones.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
    return render_to_response('miembros/crear_escalafon.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
            return HttpResponseRedirect("/miembro/listar_escalafones/")

    else:
        form = FormularioCrearEscalafon(instance=escalafon)
        return render_to_response("miembros/crear_escalafon.html", locals(), context_instance=RequestContext(request))

    # return HttpResponseRedirect("/miembro/listar_escalafones/")
    return render_to_response("miembros/crear_escalafon.html", locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def promoverMiembroEscalafon(request):
    """Promueve un miembro de escalafon siempre y cuando este cumpla con los requesitos para el cambio."""

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        form = FormularioPromoverEscalafon(data=request.POST)
        if form.is_valid():
            nuevoCambioEscalafon = form.save(commit=False)
            miembroEditar = nuevoCambioEscalafon.miembro
            if calcularCelulas(miembroEditar) >= nuevoCambioEscalafon.escalafon.celulas:
                nuevoCambioEscalafon.save()
                ok = True
            else:
                messages.error(request,
                               "El miembro %s no cumple con los requisitos para el cambio." % (str(miembroEditar)))
    else:
        form = FormularioPromoverEscalafon()
    return render_to_response('miembros/promover_escalafon.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
    return render_to_response('miembros/crear_tipo_miembro.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listarTipoMiembro(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":
        if 'editar' in request.POST:
            request.session['seleccionados'] = request.POST.getlist('seleccionados')
            return HttpResponseRedirect('/miembro/editar_tipo_miembro/')
        if 'eliminar' in request.POST:
            okElim = eliminar(request, TipoMiembro, request.POST.getlist('seleccionados'))
    tipos = list(TipoMiembro.objects.all().order_by('nombre'))
    return render_to_response('miembros/listar_tipo_miembro.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
        return render_to_response(
            "miembros/crear_tipo_miembro.html", locals(), context_instance=RequestContext(request)
        )

    # return HttpResponseRedirect("/miembro/listar_tipo_miembro/")
    return render_to_response("miembros/crear_tipo_miembro.html", locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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
            nuevoCambioTipo.fecha = datetime.date.today()
            nuevoCambioTipo.autorizacion = miembro
            nuevoCambioTipo.miembro = miembroCambio
            nuevoCambioTipo.anteriorTipo = anterior
            nuevoCambioTipo.save()
            ok = True

            _possible = ['lider', 'agente', 'maestro', 'receptor', 'administrador', 'pastor']
            if nuevoCambioTipo.nuevoTipo.nombre.lower() in _possible:
                if miembroCambio.usuario is None or miembroCambio.usuario == '':
                    request.session['tipo'] = nuevoCambioTipo.nuevoTipo.nombre
                    return HttpResponseRedirect('/miembro/asignar_usuario/' + str(miembroCambio.id) + '/')
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
        form = FormularioCambioTipoMiembro(idm=int(id))
    return render_to_response('miembros/asignar_tipo_miembro.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def crearUsuarioMimembro(request, id):
    try:
        miembroCambio = Miembro.objects.get(id=id)
    except:
        raise Http404

    if miembroCambio.usuario:
        return HttpResponseRedirect("/dont_have_permissions/")

    sesion = True

    if 'tipo' not in request.session:
        sesion = False

    if request.method == "POST":
        form = FormularioAsignarUsuario(data=request.POST)
        if form.is_valid() and form.cleaned_data['contrasena'] == form.cleaned_data['contrasenaVerificacion']:
            nuevoUsuario = User()
            if form.cleaned_data['email'] != miembroCambio.email:
                miembroCambio.correo = form.cleaned_data['email']
            nuevoUsuario.username = form.cleaned_data['email']
            nuevoUsuario.email = form.cleaned_data['email']
            nuevoUsuario.set_password(form.cleaned_data['contrasena'])
            nuevoUsuario.save()
            miembroCambio.usuario = nuevoUsuario
            miembroCambio.save()
            if sesion:
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
            return redirect(reverse('miembros:editar_perfil', args=(miembroCambio.id)))
    else:
        form = FormularioAsignarUsuario()
    form.email = miembroCambio.email
    return render_to_response('miembros/asignar_usuario.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def graduarAlumno(request):
    miembro = Miembro.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = FormularioCumplimientoPasosMiembro(data=request.POST)
        if form.is_valid():
            estudianteGraduado = form.save(commit=False)
            estudianteGraduado.paso = Pasos.objects.get(nombre__iexact="lanzamiento")
            try:
                estudiante = Matricula.objects.get(estudiante=estudianteGraduado.miembro)
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
        puedeVer = True
        form = FormularioCumplimientoPasosMiembro()
    return render_to_response('miembros/graduar_estudiante.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def eliminarCambioTipoMiembro(request, id):
    """
    El cambio que se va a eliminar se guarda en la var cambio y si esta es un
    tipo de cambio aceptable, es eliminado. En caso de que el usuario no cuente
    con ningún otro tipo de miembro luego de eliminar el cambio. El usuario será
    eliminado y no podrá loguearse en el sistema.
    """

    miembro = Miembro.objects.get(usuario=request.user)
    try:
        cambio = CambioTipo.objects.get(id=id)
    except:
        raise Http404

    if cambio.nuevoTipo.nombre.lower() == "lider":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Lider'))
    elif cambio.nuevoTipo.nombre.lower() == "agente":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Agente'))
    elif cambio.nuevoTipo.nombre.lower() == "maestro":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Maestro'))
    elif cambio.nuevoTipo.nombre.lower() == "receptor":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Receptor'))
    elif cambio.nuevoTipo.nombre.lower() == "administrador":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Administrador'))
    elif cambio.nuevoTipo.nombre.lower() == "pastor":
        cambio.miembro.usuario.groups.remove(Group.objects.get(name__iexact='Pastor'))

    try:
        if cambio.miembro.usuario.groups.count() == 0:
            if hasattr(cambio.miembro.usuario, 'empleado'):
                if not cambio.miembro.usuario.empleado:
                    cambio.miembro.usuario.delete()
            else:
                cambio.miembro.usuario.delete()
            cambio.miembro.usuario = None
            cambio.miembro.save()
    except:
        pass
    cambio.delete()
    # return HttpResponseRedirect('/miembro/perfil/' + str(cambio.miembro.id))


# TODO eliminar
def calcularCelulas(miembro):
    celulas = 0
    if miembro.grupo_lidera:
        celulas = miembro.grupo_lidera.get_descendant_count() + 1
    return celulas


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def administracion(request):
    miembro = Miembro.objects.get(usuario=request.user)
    totalGrupos = Grupo.objects.all().count()
    totalGruposA = Grupo.objects.activos().count()
    totalGruposI = Grupo.objects.inactivos().count()
    totalMiembros = Miembro.objects.all().count()
    totalMiembrosA = Miembro.objects.filter(estado='A').count()
    totalMiembrosR = Miembro.objects.filter(estado='R').count()
    totalMiembrosI = Miembro.objects.filter(estado='I').count()
    totalLideres = CambioTipo.objects.filter(nuevoTipo=TipoMiembro.objects.get(nombre__iexact="Lider")).count()
    totalMaestros = CambioTipo.objects.filter(nuevoTipo=TipoMiembro.objects.get(nombre__iexact="Maestro")).count()
    totalCursos = Curso.objects.all().count()
    totalCursosA = Curso.objects.filter(estado='A').count()
    totalCursosC = Curso.objects.filter(estado='C').count()
    # visitantes = request.session['visitantes']
    return render_to_response('miembros/administracion.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def AgregarDetalleLlamada(request):
    miembro = Miembro.objects.get(usuario=request.user)
    accion = 'Crear'
    if request.method == 'POST':
        form = FormularioDetalleLlamada(data=request.POST)
        if form.is_valid():
            NuevoDetalleLlamada = form.save()
            ok = True
    else:
        form = FormularioDetalleLlamada()
    return render_to_response(
        'miembros/agregar_detalle_llamada.html', locals(), context_instance=RequestContext(request)
    )


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listarDetallesLlamada(request):
    miembro = Miembro.objects.get(usuario=request.user)

    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(request, DetalleLlamada, request.POST.getlist('seleccionados'))

    detallesLlamada = list(DetalleLlamada.objects.all())

    return render_to_response(
        'miembros/listar_detalles_llamada.html', locals(), context_instance=RequestContext(request)
    )


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
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

    return render_to_response(
        "miembros/agregar_detalle_llamada.html", locals(), context_instance=RequestContext(request)
    )


@login_required
@permission_required('miembros.cumplimiento_pasos', raise_exception=True)
def cumplimientoPasos(request):
    """
    Permite a un Administrador o a un Agente registrar los cumplimientos de los pasos de los miembros.
    Una vez seleccionado un paso, se muestran los miembros que pueden realizar dicho paso y los que lo
    hayan realizado. La condición para que un miembro pueda realizar un paso es que haya realizado todos
    los pasos con una prioridad menor al escogido.
    """

    if request.method == 'POST':
        if 'verMiembros' in request.POST or 'promoverPaso' in request.POST:
            try:
                pasoE = Pasos.objects.get(id=request.POST.getlist('menuPasos')[0])
                numPasos = Pasos.objects.filter(prioridad__lt=pasoE.prioridad).count()

                if 'promoverPaso' in request.POST:
                    miembros = Miembro.objects.exclude(
                        pasos__prioridad__gt=pasoE.prioridad).annotate(
                            nPasos=Count('pasos')).filter(nPasos__gte=numPasos).order_by('nombre')
                    seleccionados = request.POST.getlist('seleccionados')
                    for m in miembros:
                        if str(m.id) in seleccionados:
                            if not m.pasos.filter(id=pasoE.id).exists():
                                c = CumplimientoPasos.objects.create(
                                    miembro=m, paso=pasoE, fecha=datetime.datetime.now())
                                ok = True
                        else:
                            if m.pasos.filter(id=pasoE.id).exists():
                                CumplimientoPasos.objects.get(miembro=m, paso=pasoE).delete()
                                ok = True

                miembros = Miembro.objects.exclude(
                    pasos__prioridad__gt=pasoE.prioridad).annotate(
                        nPasos=Count('pasos')).filter(nPasos__gte=numPasos).order_by('nombre')
                for m in miembros:
                    if m.pasos.filter(id=pasoE.id).exists():
                        m.cumplio = True
                    else:
                        m.cumplio = False
            except:
                raise Http404
    miembro = Miembro.objects.get(usuario=request.user)
    pasos = Pasos.objects.all().exclude(nombre__iexact='lanzamiento').order_by('prioridad', 'nombre')
    return render_to_response("miembros/cumplimiento_pasos.html", locals(), context_instance=RequestContext(request))


def recuperar_contrasena(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/iniciar_sesion')

    def _generate_password(pswd, length):
        import random
        pswd = ''
        _abc = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz1234567890'

        if isinstance(pswd, str):
            for x in range(length):
                pswd += random.choice(_abc)
            return pswd

    SUBJECT = "Recuperar Contraseña de %s" % Site.objects.get_current().name
    MESSAGE = """Ingresa al siguiente link para cambiar tu contraseña:\n
        http://%s/iniciar_sesion/?next=/miembro/cambiar_contrasena/\n\n\n
        Usuario: '%s'\n
        Nueva Contraseña: '%s' \n\n\n
        Por favor no reenviar este correo"""
    SENDER = "iglesia@mail.webfaction.com"
    RECEPT = "%s"
    ok = False

    if request.method == 'POST':
        if 'aceptar' in request.POST:
            new_password = ''
            form = FormularioRecuperarContrasenia(request.POST or None)

            if form.is_valid():
                email = form.cleaned_data['email']
                try:
                    usuario = User.objects.get(username__exact=email)
                    new_password = _generate_password(new_password, 12)

                    usuario.set_password(new_password)
                    usuario.save()

                    try:
                        send_mail(SUBJECT,
                                  MESSAGE % (request.META['HTTP_HOST'], usuario.username, new_password),
                                  SENDER,
                                  (RECEPT % email,),
                                  fail_silently=False)
                        ok = True
                    except:
                        messages.error(request, "Ha Ocurrido un problema interno...")

                except User.DoesNotExist:
                    # raise Http404
                    messages.error(request,
                                   "Usuario no encontrado, rectifica tu usuario para poder recuperar tu contraseña")

        else:
            form = FormularioRecuperarContrasenia()

    else:
        form = FormularioRecuperarContrasenia()

    return render_to_response("miembros/recuperar_contrasena.html", locals(), context_instance=RequestContext(request))


@login_required
def ver_discipulos(request, pk=None):
    d = True
    miembro = Miembro.objects.get(usuario=request.user)
    mismo = True
    if pk:
        try:
            miembro = Miembro.objects.get(id=pk)
            mismo = False
            if Miembro.objects.get(usuario=request.user).id == miembro.id:
                mismo = True
        except Miembro.DoesNotExist:
            raise Http404

    grupo = miembro.grupo_lidera or None

    if request.method == 'POST':
        if grupo is not None or grupo != '':
            form = FormularioEditarDiscipulado(request.POST or None, instance=grupo)

            if form.is_valid():
                form.save()
                # return HttpResponseRedirect('')
                ok = True
                ms = "Discipulado del grupo %s editado Correctamente" % grupo.nombre
                if mismo:
                    ms = "Tu Discipulado ha sido editado Correctamente"
            else:
                ms = "Ocurrió un Error, Por Favor Verifica el Formulario"
    else:
        if grupo is not None or grupo != '':
            form = FormularioEditarDiscipulado(instance=grupo)

    # discipulos = miembro.discipulos()
    if grupo is not None:
        discipulos = grupo.discipulos
        if len(discipulos) > 0:
            discipulos = discipulos.order_by('nombre')
        else:
            no_discipulos = True

    return render_to_response("miembros/discipulos_perfil.html", locals(), context_instance=RequestContext(request))


@login_required
@transaction.atomic
def ver_informacion_miembro(request, pk=None):
    i = True
    miembro = Miembro.objects.get(usuario=request.user)
    mismo = True
    if pk:
        try:
            miembro = Miembro.objects.get(id=pk)
            mismo = False
            if Miembro.objects.get(usuario=request.user).id == miembro.id:
                mismo = True
        except Miembro.DoesNotExist:
            raise Http404

    if request.user.has_perm('miembros.es_administrador'):
        if request.method == 'POST':
            if 'rllamada' in request.POST:
                data = {'id': miembro.id}
                request.session['perfil'] = True
                request.session['miembrosSeleccionados'] = [miembro.id]
                return HttpResponseRedirect('/miembro/registrar_llamada/agente/')

            form = FormularioInformacionIglesiaMiembro(request.POST, instance=miembro)
            form_cambio_tipo = FormularioTipoMiembros(request.POST, instance=miembro)

            if form.is_valid() and form_cambio_tipo.is_valid():
                form.save()
                tipos = form_cambio_tipo.cleaned_data['tipos']
                tpvisita = TipoMiembro.objects.get(nombre__iexact='visita')
                tpmiembro = TipoMiembro.objects.get(nombre__iexact='miembro')
                tplider = TipoMiembro.objects.get(nombre__iexact='lider')

                cambio = CambioTipo.objects.filter(miembro=miembro)
                tipos_cambio = [c.nuevoTipo for c in cambio]
                eliminar = [cambio_iter for cambio_iter in tipos_cambio if cambio_iter not in tipos]

                if len(eliminar):
                    for e in eliminar:
                        try:
                            c = CambioTipo.objects.get(miembro=miembro, nuevoTipo=e)
                        except:
                            c = CambioTipo.objects.get(miembro=miembro, anteriorTipo=e)
                        eliminarCambioTipoMiembro(request, c.id)
                    cambio = CambioTipo.objects.filter(miembro=miembro)
                    tipos_cambio = [c_iter.nuevoTipo for c_iter in cambio]

                for tipo in tipos:
                    if tipo not in tipos_cambio:
                        cambio = CambioTipo()
                        cambio.miembro = miembro
                        cambio.autorizacion = Miembro.objects.get(usuario=request.user)
                        cambio.fecha = date.today()
                        if tipo not in tipos_cambio:
                            if tipo == tpvisita:
                                cambio.anteriorTipo = tipo
                            elif tipo == tpmiembro:
                                cambio.anteriorTipo = tpvisita
                            elif tipo == tplider:
                                cambio.anteriorTipo = tpmiembro
                            else:
                                cambio.anteriorTipo = tipo
                        if tipo not in [tpvisita, tpmiembro]:
                            if not cambio.miembro.usuario:
                                import re
                                cedula = re.findall(r'\d+', cambio.miembro.cedula)
                                cedula = ''.join(cedula)
                                try:
                                    usuario = User.objects.get(email=cambio.miembro.email)
                                except:
                                    usuario = User()
                                    usuario.username = '{}'.format(cambio.miembro.cedula)
                                    usuario.email = cambio.miembro.email
                                usuario.set_password(cedula)
                                usuario.save()
                                cambio.miembro.usuario = usuario
                                cambio.miembro.save()
                            if tipo == tplider:
                                cambio.miembro.usuario.groups.add(Group.objects.get(name__iexact='lider'))
                            elif tipo == TipoMiembro.objects.get(nombre__iexact='agente'):
                                cambio.miembro.usuario.groups.add(Group.objects.get(name__iexact='Agente'))
                            elif tipo == TipoMiembro.objects.get(nombre__iexact='maestro'):
                                cambio.miembro.usuario.groups.add(Group.objects.get(name__iexact='Maestro'))
                            elif tipo == TipoMiembro.objects.get(nombre__iexact='receptor'):
                                cambio.miembro.usuario.groups.add(Group.objects.get(name__iexact='Receptor'))
                            elif tipo == TipoMiembro.objects.get(nombre__iexact='administrador'):
                                cambio.miembro.usuario.groups.add(Group.objects.get(name__iexact='Administrador'))
                            elif tipo == TipoMiembro.objects.get(nombre__iexact='pastor'):
                                cambio.miembro.usuario.groups.add(Group.objects.get(name__iexact='Pastor'))
                            cambio.miembro.usuario.save()
                        cambio.nuevoTipo = tipo
                        cambio.save()
                    else:
                        # return HttpResponse(eliminar, content_type='text/plain')
                        continue

                ok = True
                ms = "Miembro %s %s Editado Correctamente" % (miembro.nombre.upper(), miembro.primerApellido.upper())
                if mismo:
                    ms = "Te has Editado Correctamente"
                # return redirect(reverse('miembros:ver_informacion', args=(miembro.id, )))
            else:
                if form_cambio_tipo.errors:
                    form.add_error('estado', 'Error en formulario')
                ms = "Ocurrió un Error, Por Favor Verifica el Formulario"
        else:
            form = FormularioInformacionIglesiaMiembro(instance=miembro)
            form_cambio_tipo = FormularioTipoMiembros(instance=miembro)

    if miembro.grupo:
        lideres_miembro = miembro.grupo.lideres.all()
    escalafones = list(CambioEscalafon.objects.filter(miembro=miembro).order_by('fecha'))
    tipos = CambioTipo.objects.filter(miembro=miembro).order_by('-fecha')
    if len(escalafones) > 0:
        escalafon = escalafones.pop()
    pasos = list(CumplimientoPasos.objects.filter(miembro=miembro).order_by('fecha'))

    return render_to_response("miembros/informacion_perfil.html", locals(), context_instance=RequestContext(request))


@login_required
def eliminar_foto_perfil(request, pk):
    miembro = Miembro.objects.get(usuario=request.user)
    # mismo = True
    response = {}

    if pk:
        try:
            miembro = Miembro.objects.get(pk=pk)
            # mismo = False
            if Miembro.objects.get(usuario=request.user).id == miembro.id:
                # mismo = True
                pass
        except Miembro.DoesNotExist:
            raise Http404

    foto = False
    if miembro.foto_perfil:
        rut_perfil = miembro.foto_perfil.path
        foto = True
    if request.method == 'POST':
        if 'delete_file' in request.POST:
            if miembro.foto_perfil != '' or miembro.foto_perfil is not None:
                if foto:
                    if os.path.exists(rut_perfil):
                        print("si existe")
                    if os.path.isfile(rut_perfil):
                        print("Es archivo")
                        os.remove(rut_perfil)
                    try:
                        miembro.foto_perfil.delete(save=True)
                        response['status'] = 'warning'
                        response['ruta'] = settings.STATIC_URL + 'Imagenes/profile-none.jpg'
                        response['ms'] = 'Foto Eliminada Exitosamente'
                    except:
                        response['status'] = 'danger'
                        response['ruta'] = settings.STATIC_URL + 'Imagenes/profile-none.jpg'
                        response['ms'] = 'Hubo un error al intentar eliminar la foto'
                else:
                    response['status'] = 'danger'
                    response['ruta'] = settings.STATIC_URL + 'Imagenes/profile-none.jpg'
                    response['ms'] = 'No hay ninguna foto a eliminar'
            else:
                response['status'] = 'warning'
                response['ruta'] = settings.STATIC_URL + 'Imagenes/profile-none.jpg'
                response['ms'] = 'No hay fotos para eliminar'
        else:
            response['status'] = 'danger'
            response['ruta'] = settings.STATIC_URL + 'Imagenes/profile-none.jpg'
            response['ms'] = 'Permiso denegado para hacer esta operacion'
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def crear_miembro(request):
    """
    Permite crear miembros para una iglesia.
    """

    if request.method == 'POST':
        form = NuevoMiembroForm(data=request.POST)
        if form.is_valid():
            form.save(request.iglesia)
            messages.success(request, _('El miembro se ha creado correctamente'))
            return redirect('miembros:nuevo')
    else:
        form = NuevoMiembroForm()

    return render(request, 'miembros/miembro_form.html', {'form': form})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listar_lideres(request, pk):
    """
    Permite a un administrador listar los lideres de la red escogida.
    """

    red = get_object_or_404(Red, pk=pk)
    lideres = Miembro.objects.lideres_red(red).select_related('usuario', 'grupo_lidera')

    return render(request, 'miembros/lista_lideres.html', {'red': red, 'lideres': lideres})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def trasladar(request, pk):
    """
    Permite a un administrador trasladar un miembro que no lidere grupo a que asista a otro grupo.
    """

    miembro = get_object_or_404(Miembro, pk=pk)
    if miembro.grupo_lidera:
        return redirect(reverse('sin_permiso'))

    if request.method == 'POST':
        form = TrasladarMiembroForm(data=request.POST)
        if form.is_valid():
            form.trasladar(miembro)
            return redirect('miembros:trasladar', pk)
    else:
        form = TrasladarMiembroForm()

    return render(request, 'miembros/trasladar.html', {'miembro': miembro, 'form': form})
