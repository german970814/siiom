'''
Created on 4/04/2011

@author: Conial
'''
from datetime import date
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test, login_required
from miembros.models import Miembro, TipoMiembro
from django.template.context import RequestContext
from grupos.models import Grupo
from django.db.models import Q
from miembros.models import CambioTipo, CumplimientoPasos, Pasos
from common.decorators import permisos_requeridos


def inicio(request):
    return HttpResponseRedirect('/iniciar_sesion/')


def custom_404(request):
    return render_to_response('404.html')


def without_perms(request):
    if not request.user.is_authenticated():
        request.session['next'] = request.GET.get('next', '')
        return HttpResponseRedirect('/iniciar_sesion/')
    return render_to_response("without_perms.html", locals(), context_instance=RequestContext(request))


def mapa(request):
    return render_to_response("mapas.html", locals(), context_instance=RequestContext(request))


# ---------------------------------------

@login_required
@permisos_requeridos('miembros.es_lider', 'miembros.buscar_todos')
def buscar(request, tipo):
    """
    Permite realizar busqueda de miembros por nombre, apellido y/o identificación y grupos por sus lideres. El tipo
    (miembro, grupo) indica si se va a buscar miembros o grupos. Si el usuario no tiene permiso de buscar todos, los
    resultados solo estaran dentro de sus descendientes.
    """

    resultados = []
    termino_busqueda = request.GET.get('buscar')
    if termino_busqueda:
        terminos = termino_busqueda.split()
        q = (
            Q(nombre__icontains=terminos[0]) | Q(primerApellido__icontains=terminos[0]) |
            Q(segundoApellido__icontains=terminos[0]) | Q(cedula=terminos[0])
        )

        for termino in terminos[1:]:
            q.add(
                (
                    Q(nombre__icontains=termino) | Q(primerApellido__icontains=termino) |
                    Q(segundoApellido__icontains=termino) | Q(cedula=termino)
                ), Q.OR
            )

        resultados = Miembro.objects.select_related('grupo_lidera', 'grupo').filter(q)

        # Solo se buscan los miembros que pertenezcan a la red del usuario logueado sino tiene permiso de buscar todos.
        if not request.user.has_perm('miembros.buscar_todos'):
            grupo = Miembro.objects.get(usuario=request.user).grupo_lidera
            if grupo:
                red_miembro = Grupo.get_tree(grupo)
                resultados = resultados.filter(Q(grupo__in=red_miembro) | Q(grupo_lidera__in=red_miembro))
            else:
                resultados = Miembro.objects.none()

        if tipo == 'grupo':  # Si el tipo de busqueda es de grupos, se filtran según los lideres.
            resultados = Grupo.objects.prefetch_related('lideres').filter(lideres__in=resultados)

    return render(request, 'buscar.html', {'tipo': tipo, 'resultados': resultados, 'termino': termino_busqueda})
