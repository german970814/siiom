# Django Imports
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.conf import settings
from django.core.urlresolvers import reverse

# Third-Party App Imports
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin, PermissionRequiredMixin

# Apps Imports
from common.decorators import permisos_requeridos
from .models import Grupo, ReunionGAR, ReunionDiscipulado, Red, AsistenciaDiscipulado, Predica
from .forms import (
    FormularioEditarGrupo, FormularioReportarReunionGrupo,
    FormularioReportarReunionDiscipulado, FormularioCrearRed, FormularioSetGeoPosicionGrupo,
    FormularioTransladarGrupo, FormularioCrearPredica,
    FormularioReportarReunionGrupoAdmin, FormularioReportesEnviados, FormularioEditarReunionGAR,
    GrupoRaizForm, NuevoGrupoForm, EditarGrupoForm, TransladarGrupoForm, RedForm
)
from miembros.models import Miembro
from common.groups_tests import (
    liderTest, adminTest, verGrupoTest, receptorAdminTest, PastorAdminTest, admin_or_director_red
)
from .utils import reunion_reportada, obtener_fechas_semana

# Python Packages
import datetime
import json
import copy


@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def editarHorarioReunionGrupo(request, pk=None):
    g = True
    miembro = Miembro.objects.get(usuario=request.user)
    mismo = True
    draw_mapa = True
    # grupo.miembro_set.all()
    if pk:
        try:
            miembro = Miembro.objects.get(id=pk)
            mismo = False
            if Miembro.objects.get(usuario=request.user).id == miembro.id:
                mismo = True
        except Miembro.DoesNotExist:
            raise Http404

    grupo = miembro.grupo_lidera
    if mismo:
        puede_editar = True
    if grupo is None:
        puede_editar = False
        grupo = miembro.grupo
        no_lider = True
    if grupo is not None:
        miembros = grupo.miembrosGrupo()
        lideres = grupo.lideres.all()
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

    return render_to_response('grupos/editar_grupo.html', locals(), context_instance=RequestContext(request))


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
    grupo = miembro.grupo_lidera

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
                reportada = reunion_reportada(reunion.fecha, grupo)  # esta variable es enviada al template

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
                    return redirect('miembros:reportar_reunion_grupo')
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
    return render_to_response('grupos/reportar_reunion_grupo.html', locals(), context_instance=RequestContext(request))


@user_passes_test(admin_or_director_red, login_url="/dont_have_permissions/")
def reportarReunionGrupoAdmin(request):

    if request.method == 'POST':
        form = FormularioReportarReunionGrupoAdmin(data=request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reportada = reunion_reportada(reunion.fecha, reunion.grupo)
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
                return redirect('miembros:reportar_reunion_grupo_admin')
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
    return render_to_response('grupos/reportar_reunion_grupo_admin.html', locals(), context_instance=RequestContext(request))


@user_passes_test(liderTest, login_url="/dont_have_permissions/")
def reportarReunionDiscipulado(request):
    miembro = Miembro.objects.get(usuario=request.user)
    grupo = miembro.grupo_lidera
    if grupo:
        discipulos = grupo.discipulos
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
    return render_to_response('grupos/reportar_reunion_discipulado.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def listarRedes(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == "POST":

        if 'eliminar' in request.POST:
            okElim = eliminar(request, Red, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')
    redes = list(Red.objects.all())

    return render_to_response('grupos/listar_redes.html', locals(), context_instance=RequestContext(request))


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
    return render_to_response('grupos/crear_red.html', locals(), context_instance=RequestContext(request))


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
        return render_to_response("grupos/crear_red.html", locals(), context_instance=RequestContext(request))

    return render_to_response("grupos/crear_red.html", locals(), context_instance=RequestContext(request))


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
    return render_to_response('grupos/listar_predicas.html', locals(), context_instance=RequestContext(request))


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
    return render_to_response('grupos/crear_predica.html', locals(), context_instance=RequestContext(request))


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
        return render_to_response("grupos/crear_predica.html", locals(), context_instance=RequestContext(request))

    return render_to_response("grupos/crear_predica.html", locals(), context_instance=RequestContext(request))


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


# TODO eliminar
def listaGruposDescendientes(grupo):
    """Devuelve una lista con todos los grupos descendientes del grupo del miembro usado como parametro para ser
        usada en un choice field."""

    miembro = grupo.lideres.first()
    listaG = [grupo]
    discipulos = list(miembro.discipulos())
    while len(discipulos) > 0:
        d = discipulos.pop(0)
        g = d.grupo_lidera()
        if g:
            if g not in listaG:
                listaG.append(g)
            lid = g.lideres.all()
            for l in lid:  # Se elimina los otros lideres de la lista de discipulos para que no se repita el grupo.
                if l in discipulos:
                    discipulos.remove(l)
        if d.discipulos():  # Se agregan los discipulos del miembro en la lista de discipulos.
            discipulos.extend(list(d.discipulos()))
    return listaG


def sendMail(camposMail):
    subject = camposMail[0]
    mensaje = camposMail[1]
    receptor = camposMail[2]
    send_mail(subject, mensaje, 'iglesia@mail.webfaction.com', receptor, fail_silently=False)


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


@user_passes_test(admin_or_director_red, login_url="/dont_have_permissions/")
def ver_reportes_grupo(request):
    if request.method == 'POST' or (
        'post' in request.session and len(request.session['post']) > 1 and request.session.get('valid_post', False)
       ):
        if 'combo' in request.POST:
            value = request.POST['value']
            querys = Q(lideres__nombre__icontains=value) | Q(lideres__primerApellido__icontains=value) | \
                Q(lideres__cedula__icontains=value)
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
                reportada = reunion_reportada(reunion.fecha, reunion.grupo)

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
                    return redirect('grupos:reportes_grupo')
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
                return redirect('grupos:reportes_grupo')

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

    return render_to_response("grupos/ver_reportes_grupo.html", locals(), context_instance=RequestContext(request))


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
                reportada = reunion_reportada(reunion_formulario.fecha, reunion_formulario.grupo)

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
                        <a href="%(link)s" class="alert-link">Volver a reuniones.</a>' % {'link': reverse('grupos:reportes_grupo')})
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
                    <a href="%(link)s" class="alert-link">Volver a reuniones.</a>' % {'link': reverse('grupos:reportes_grupo')})
                )
        else:
            messages.error(request, _('Ha ocurrido un error al enviar el formulario, verifica los campos'))

    else:
        form = FormularioEditarReunionGAR(instance=reunion)

    return render_to_response("grupos/editar_reunion_grupo.html", locals(), context_instance=RequestContext(request))


def set_position_grupo(request, id_grupo):
    """
    Vista para setear la posicion de un grupo.
    """

    grupo = get_object_or_404(Grupo, id=id_grupo)

    data = {}

    # latitud = request.GET.get('lat', None)
    # longitud = request.GET.get('long', None)
    form = FormularioSetGeoPosicionGrupo(data=request.GET, instance=grupo)

    if form.is_valid():
        form.save()
        data['code_response'] = 200
        data['message'] = 'Grupo %s editado correctamente' % grupo.get_nombre()
    else:
        data['error'] = form.errors
        data['code_response'] = 400

    return HttpResponse(json.dumps(data), content_type='application/json')

# -----------------------------------


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
@permisos_requeridos('miembros.buscar_todos', 'miembros.es_lider')
def detalle_grupo(request, pk):
    """
    Permite ver el detalle de un grupo. Si el usuario no puede buscar todos solo podrá ver sus descendientes.
    """

    grupo = get_object_or_404(Grupo, pk=pk)
    if not request.user.has_perm('miembros.buscar_todos'):
        grupo_lidera = Miembro.objects.get(usuario=request.user).grupo_lidera
        if grupo_lidera:
            if not grupo.is_descendant_of(grupo_lidera) and grupo_lidera != grupo:
                raise PermissionDenied
        else:
            raise PermissionDenied

    return render(request, 'grupos/detalle_grupo.html', {'grupo': grupo})


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
                messages.success(request, _('El grupo se ha creado correctamente.'))
                return redirect('grupos:listar', pk)
    else:
        form = NuevoGrupoForm(red=red)

    return render(request, 'grupos/grupo_form.html', {'form': form})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def editar_grupo(request, pk):
    """
    Permite a un administrador editar un grupo de una iglesia.
    """

    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == 'POST':
        form = EditarGrupoForm(instance=grupo, data=request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, _('El grupo se ha editado correctamente.'))
                return redirect('grupos:listar', grupo.red.id)
    else:
        form = EditarGrupoForm(instance=grupo)

    return render(request, 'grupos/grupo_form.html', {'form': form})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def listar_grupos(request, pk):
    """
    Permite a un administrador listar los grupos de la red escogida.
    """

    red = get_object_or_404(Red, pk=pk)
    grupos = Grupo.objects.prefetch_related('lideres').red(red)
    return render(request, 'grupos/lista_grupos.html', {'red': red, 'grupos': grupos})


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


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def sin_confirmar_ofrenda_GAR(request):
    """
    Permite a un administrador listar los grupos que faltan por confirmar la ofrenda de las reuniones GAR.
    """

    grupos = Grupo.objects.sin_confirmar_ofrenda_GAR().prefetch_related('lideres')
    return render(request, 'grupos/sin_confirmar_ofrenda_GAR.html', {'grupos': grupos})


@login_required
@permission_required('grupos.puede_confirmar_ofrenda_GAR', raise_exception=True)
def confirmar_ofrenda_GAR(request, pk):
    """
    Permite a un administrador o receptor confirmar la ofrenda de la reunión GAR del grupo especificado.
    """

    grupo = get_object_or_404(Grupo, pk=pk)

    if request.method == 'POST':
        reuniones_confirmar = request.POST.getlist('seleccionados')
        grupo.confirmar_ofrenda_reuniones_GAR(reuniones_confirmar)
        messages.success(request, _('Se han confirmado las reuniones escogidas.'))
        return redirect('grupos:confirmar_ofrenda_GAR', pk)
    else:
        reuniones = grupo.reuniones_GAR_sin_ofrenda_confirmada

    return render(request, 'grupos/confirmar_ofrenda_GAR.html', {'reuniones': reuniones})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def sin_confirmar_ofrenda_discipulado(request):
    """
    Permite a un administrador listar los grupos que faltan por confirmar la ofrenda de las reuniones de discipulado.
    """

    grupos = Grupo.objects.sin_confirmar_ofrenda_discipulado().prefetch_related('lideres')
    return render(request, 'grupos/sin_confirmar_ofrenda_discipulado.html', {'grupos': grupos})


@login_required
@permission_required('grupos.puede_confirmar_ofrenda_discipulado', raise_exception=True)
def confirmar_ofrenda_discipulado(request, pk):
    """
    Permite a un administrador o receptor confirmar la ofrenda de la reunión de discipulado del grupo especificado.
    """

    grupo = get_object_or_404(Grupo, pk=pk)

    if request.method == 'POST':
        reuniones_confirmar = request.POST.getlist('seleccionados')
        grupo.confirmar_ofrenda_reuniones_discipulado(reuniones_confirmar)
        messages.success(request, _('Se han confirmado las reuniones escogidas.'))
        return redirect('grupos:confirmar_ofrenda_discipulado', pk)
    else:
        reuniones = grupo.reuniones_discipulado_sin_ofrenda_confirmada

    return render(request, 'grupos/confirmar_ofrenda_discipulado.html', {'reuniones': reuniones})


@login_required
@permission_required('miembros.es_administrador', raise_exception=True)
def crear_red(request):
    """
    Permite a un administrador crear una red de una iglesia.
    """

    if request.method == 'POST':
        form = RedForm(data=request.POST)
        if form.is_valid():
            form.save(request.iglesia)
            messages.success(request, _('La red se ha creado correctamente.'))
            return redirect('grupos:red_nueva')
    else:
        form = RedForm()

    return render(request, 'grupos/red_form.html', {'form': form, 'VERBO': 'Crear'})
