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
from miembros.forms import FormularioCumplimientoPasosMiembro
from miembros.models import CambioTipo, CumplimientoPasos, Pasos
from miembros.views import cambiarContrasena


def inicio(request):
    return HttpResponseRedirect('/iniciar_sesion/')

def miembroTest(user):
    return  user.is_authenticated() \
            and (Group.objects.get(name__iexact='Maestro') in user.groups.all()\
            or Group.objects.get(name__iexact='Lider') in user.groups.all()    \
            or Group.objects.get(name__iexact='Agente') in user.groups.all()   \
            or Group.objects.get(name__iexact='Receptor') in user.groups.all()
            or Group.objects.get(name__iexact='Administrador') in user.groups.all())

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
            resultadosMiembros.extend(list(Miembro.objects.filter(Q(nombre__icontains=st) | Q(cedula=st) | Q(primerApellido__icontains=st) | Q(segundoApellido__icontains=st) ).order_by("nombre")))
            resultadosGrupos.extend(list(Grupo.objects.filter(nombre__icontains=st).order_by("nombre")))
        
        resultadosMiembros = list(set(resultadosMiembros))
        resultadosGrupos = list(set(resultadosGrupos))
        
        if miembro.usuario.has_perm("miembros.buscar_todos"):
            resultados = []
            for r in resultadosMiembros:
                resultados.append({"resultado":r, "model_name":"miembro"})
                
            for r in resultadosGrupos:
                resultados.append({"resultado":r, "model_name":"grupo"})
        else:
            resultados = []
            discipulos = list(miembro.discipulos())
            for discipulo in discipulos:
                subdiscipulos = discipulo.discipulos()
                for subd in subdiscipulos:
                    discipulos.append(subd)
            
            for r in resultadosMiembros:
                if r in discipulos:
                    resultados.append({"resultado":r, "model_name":"miembro"})
                
            for r in resultadosGrupos:
                if r.lider1 in discipulos or r.lider2 in discipulos:
                    resultados.append({"resultado":r, "model_name":"grupo"})

        return render_to_response('resultado_busqueda.html', locals(), context_instance=RequestContext(request))
    
    return HttpResponseRedirect('/miembro/')

def depu(request):
    padre = Miembro.objects.get(id = 1)
    miembros = Miembro.objects.all().order_by('id')
    cad = ''
    print(miembros)
    print(padre)
    for m in miembros:
        if m.email!='NN':
            cad = cad+m.email+'<br />'
            if m.usuario==None:
                user = User.objects.create()
                user.username = m.email
                user.set_password(123456)
                user.save()
                m.usuario = user

            if m.conyugue != None and m.conyugue != '':
                con = Miembro.objects.get(id = m.conyugue.id)
                con.conyugue = m
                con.estadoCivil = 'C'
                con.save()
                m.estadoCivil = 'C'

            m.save()
            print(m)

            cambioTipo = CambioTipo.objects.create(miembro=m, autorizacion=padre, nuevoTipo=TipoMiembro.objects.get(nombre__iexact="lider"), anteriorTipo=TipoMiembro.objects.get(nombre__iexact="visita"), fecha=date.today())
            print(cambioTipo)
            cambioTipo.save()

            m.usuario.groups.add(Group.objects.get(name__iexact='Lider'))
            
            cp = CumplimientoPasos.objects.create(miembro=m, paso=Pasos.objects.get(nombre__iexact = 'Lanzamiento'), fecha=date.today())
            print(cp)
            cp.save()

    return HttpResponse(cad)

def depu2(request):
    grupos = Grupo.objects.filter(nombre__iexact = 'NN')
    for g in grupos:
        g.nombre = g.lider1.primerApellido
        if g.lider2 is not None:
            g.nombre = g.nombre + " - " + g.lider2.primerApellido

        g.save()
        print(g.nombre)
    return HttpResponse(grupos)
