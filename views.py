'''
Created on 4/04/2011

@author: Conial
'''
from datetime import date
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test
from miembros.models import Miembro, TipoMiembro
from django.template.context import RequestContext
from grupos.models import Grupo
from django.db.models import Q
from miembros.models import CambioTipo, CumplimientoPasos, Pasos


def inicio(request):
    return HttpResponseRedirect('/iniciar_sesion/')


def custom_404(request):
    return render_to_response('404.html')


def miembroTest(user):
    return user.is_authenticated() and (
        Group.objects.get(name__iexact='Maestro') in user.groups.all()
        or Group.objects.get(name__iexact='Lider') in user.groups.all()
        or Group.objects.get(name__iexact='Agente') in user.groups.all()
        or Group.objects.get(name__iexact='Receptor') in user.groups.all()
        or Group.objects.get(name__iexact='Administrador') in user.groups.all()
    )


@user_passes_test(miembroTest, login_url="/iniciar_sesion/")
def resultadoBusqueda(request, tipoBus):
    miembro = Miembro.objects.get(usuario=request.user)

    if request.method == 'POST':

        try:
            sTerm = request.POST.getlist('buscar')[0]
        except:
            return HttpResponseRedirect('/miembro/')

        csTerm = sTerm.lower()
        csTerm = csTerm.split(" ")

        resultadosMiembros = []
        resultadosGrupos = []

        for st in csTerm:
            resultadosMiembros.extend(list(Miembro.objects.filter(
                Q(nombre__icontains=st) | Q(cedula=st) |
                Q(primerApellido__icontains=st) | Q(segundoApellido__icontains=st)
            ).order_by("nombre")))
            resultadosGrupos.extend(list(Grupo.objects.filter(nombre__icontains=st).order_by("nombre")))

        resultadosMiembros = list(set(resultadosMiembros))
        resultadosGrupos = list(set(resultadosGrupos))
        # print(resultadosGrupos)

        if miembro.usuario.has_perm("miembros.buscar_todos"):
            resultados = []
            for r in resultadosMiembros:
                resultados.append({"resultado": r, "model_name": "miembro"})

            for r in resultadosGrupos:
                resultados.append({"resultado": r, "model_name": "grupo"})
        else:
            resultados = []
            discipulos = list(miembro.discipulos())
            for discipulo in discipulos:
                subdiscipulos = discipulo.discipulos()
                for subd in subdiscipulos:
                    discipulos.append(subd)

            for r in resultadosMiembros:
                if r in discipulos:
                    resultados.append({"resultado": r, "model_name": "miembro"})

            for r in resultadosGrupos:
                if r.lider1 in discipulos or r.lider2 in discipulos:
                    resultados.append({"resultado": r, "model_name": "grupo"})

        return render_to_response('resultado_busqueda.html', locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect('/miembro/')


def without_perms(request):
    if not request.user.is_authenticated():
        request.session['next'] = request.GET.get('next', '')
        return HttpResponseRedirect('/iniciar_sesion/')
    return render_to_response("without_perms.html", locals(), context_instance=RequestContext(request))


def mapa(request):
    return render_to_response("mapas.html", locals(), context_instance=RequestContext(request))
