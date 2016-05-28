from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import transaction
from .forms import CrearEncuentroForm, NuevoEncontristaForm
from grupos.models import Red, Grupo
from miembros.models import Miembro, TipoMiembro
from .models import Encuentro, Encontrista
import json
from common.tests import tesorero_administrador_test, adminTest, admin_tesorero_coordinador_test
from .utils import crear_miembros_con_encontristas, avisar_tesorero_coordinador_encuentro, solo_encuentros_miembro


URL = "/dont_have_permissions/"


@user_passes_test(adminTest, login_url=URL)
def crear_encuentro(request):
    accion = 'Crear'
    if request.method == 'POST':
        if 'combo_tesorero' in request.POST:
            red = Red.objects.get(id=request.POST['id_red'])
            value = request.POST['value']
            querys = Q(nombre__icontains=value) | Q(primerApellido__icontains=value) | Q(cedula__icontains=value)
            tipo = TipoMiembro.objects.get(nombre__iexact='lider')
            miembros = Miembro.objects.filter(miembro_cambiado__nuevoTipo=tipo, estado='A')
            miembros = miembros.filter(querys)[:10]
            response = [{'pk': str(a.id), 'nombre': str(a)} for a in miembros]
            return HttpResponse(json.dumps(response), content_type='application/json')

        form = CrearEncuentroForm(data=request.POST)

        if form.is_valid():
            nuevo_encuentro = form.save()
            avisar_tesorero_coordinador_encuentro(nuevo_encuentro.tesorero, nuevo_encuentro.coordinador)
            ok = True
    else:
        form = CrearEncuentroForm()

    return render_to_response('Encuentro/crear_encuentro.html', locals(), context_instance=RequestContext(request))


@user_passes_test(tesorero_administrador_test, login_url=URL)
def obtener_grupos(request):
    if request.method == 'POST':
        if 'combo_grupo' in request.POST:
            red = Red.objects.get(id=request.POST['id_red'])
            value = request.POST.get('value', '')
            querys = Q(lider1__nombre__icontains=value) |\
                Q(lider1__primerApellido__icontains=value) | Q(lider1__cedula__icontains=value) |\
                Q(lider2__nombre__icontains=value) | Q(lider2__primerApellido__icontains=value) |\
                Q(lider2__cedula__icontains=value)
            grupos = Grupo.objects.filter(red=red)
            grupos = grupos.filter(querys)[:10]
            response = [{'pk': str(a.id), 'nombre': str(a)} for a in grupos]
            return HttpResponse(json.dumps(response), content_type='application/json')


@user_passes_test(admin_tesorero_coordinador_test, login_url=URL)
def listar_encuentros(request):
    miembro = Miembro.objects.get(usuario=request.user)
    if miembro.usuario.has_perm('miembros.es_administrador'):
        encuentros = Encuentro.objects.activos()
    elif miembro.usuario.has_perm('miembros.es_coordinador'):
        encuentros = miembro.encuentros_coordinador.activos()
    elif miembro.usuario.has_perm('miembros.es_tesorero'):
        encuentros = miembro.encuentros_tesorero.activos()

    return render_to_response('Encuentro/listar_encuentros.html', locals(), context_instance=RequestContext(request))


@user_passes_test(tesorero_administrador_test, login_url=URL)
def agregar_encontrista(request, id_encuentro):
    accion = 'Crear'
    encuentro = get_object_or_404(Encuentro, pk=id_encuentro)
    mismo = solo_encuentros_miembro(request, encuentro)
    if mismo:
        return mismo

    if request.method == 'POST':
        form = NuevoEncontristaForm(data=request.POST, encuentro=encuentro)

        if form.is_valid():
            encontrista = form.save(commit=False)
            encontrista.encuentro = encuentro
            encontrista.save()
            ok = True
    else:
        form = NuevoEncontristaForm(encuentro=encuentro)

    return render_to_response('Encuentro/agregar_encontrista.html', locals(), context_instance=RequestContext(request))


@user_passes_test(tesorero_administrador_test, login_url=URL)
def editar_encontrista(request, id_encontrista):
    accion = 'Editar'
    encontrista = get_object_or_404(Encontrista, pk=id_encontrista)
    encuentro = encontrista.encuentro
    mismo = solo_encuentros_miembro(request, encuentro)
    if mismo:
        return mismo

    if request.method == 'POST':
        form = NuevoEncontristaForm(data=request.POST, instance=encontrista)  # , encuentro=encuentro)

        if form.is_valid():
            # encontrista = form.save(commit=False)
            # encontrista.encuentro = encuentro
            form.save()
            ok = True
    else:
        form = NuevoEncontristaForm(instance=encontrista)

    return render_to_response('Encuentro/agregar_encontrista.html', locals(), context_instance=RequestContext(request))


@user_passes_test(tesorero_administrador_test, login_url=URL)
def borrar_encontrista(request, id_encontrista):
    encontrista = get_object_or_404(Encontrista, pk=id_encontrista)
    encuentro = Encuentro.objects.get(id=encontrista.encuentro.id)
    encontrista.delete()
    return HttpResponseRedirect('/encuentro/listar_encontristas/%s/' % str(encuentro.id))


@user_passes_test(admin_tesorero_coordinador_test, login_url=URL)
def listar_encontristas(request, id_encuentro):

    encuentro = get_object_or_404(Encuentro, pk=id_encuentro)
    mismo = solo_encuentros_miembro(request, encuentro)
    if mismo:
        return mismo

    encontristas = encuentro.encontrista_set.all()
    return render_to_response('Encuentro/listar_encontristas.html', locals(), context_instance=RequestContext(request))


@transaction.atomic
@user_passes_test(tesorero_administrador_test, login_url=URL)
def asistencia_encuentro(request, id_encuentro):
    encuentro = get_object_or_404(Encuentro, pk=id_encuentro)
    mismo = solo_encuentros_miembro(request, encuentro)
    if mismo:
        return mismo

    encontristas = encuentro.encontrista_set.all()
    if len(encontristas) == 0:
        mensaje = 'Este encuentro no tiene encontristas'

    if request.method == 'POST':
        if 'seleccionados' in request.POST:
            if encuentro.acabado:
                seleccionados = Encontrista.objects.filter(id__in=request.POST.getlist('seleccionados'))
                for encontrista in seleccionados:
                    encontrista.asistio = True
                    encontrista.save()
                if request.user.has_perm('miembros.es_administrador'):
                    crear_miembros_con_encontristas(seleccionados)
                return HttpResponseRedirect('/encuentro/encuentros/')
            else:
                pass
        # form

    return render_to_response('Encuentro/asistencia_encuentro.html', locals(), context_instance=RequestContext(request))
