# Create your views here.
import calendar
import datetime
from encodings.utf_8_sig import encode
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.mail import send_mail, send_mass_mail
from django.db.models import Sum, Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.datetime_safe import strftime
from grupos.models import Red, ReunionGAR, AsistenciaMiembro, Grupo, ReunionDiscipulado, AsistenciaDiscipulado
from miembros.models import Miembro, DetalleLlamada, Pasos, CumplimientoPasos, CambioTipo
from reportes.charts import PdfTemplate
from reportes.forms import FormularioRangoFechas, FormularioVisitasPorMes, FormularioVisitasRedPorMes, \
    FormularioCumplimientoLlamadasLideres
from reportes.forms import FormularioReportesSinEnviar, FormularioPredicas


def liderAdminTest(user):
    return user.is_authenticated() \
            and (Group.objects.get(name__iexact = 'Lider') in user.groups.all() \
            or Group.objects.get(name__iexact = 'Administrador') in user.groups.all())


def agenteAdminTest(user):
    return user.is_authenticated() \
            and (Group.objects.get(name__iexact = 'Agente') in user.groups.all() \
            or Group.objects.get(name__iexact = 'Administrador') in user.groups.all())


@user_passes_test(agenteAdminTest, login_url="/dont_have_permissions/")
def visitasAsignadasRedes(request):
    """Este reporte muestra el total de visitas asignadas a las distintas redes en un rango de fechas escogida
    por el usuario."""

    tipo = 1
    titulo_pag = 'Total de visitas en cada red'
    if request.method == 'POST':
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fecha_i = form.cleaned_data['fechai']
            fecha_f = form.cleaned_data['fechaf']
            opciones = {'fi': fecha_i, 'ff': fecha_f}
            sw = True

            redes = Red.objects.all()
            values = [['Red', 'Visitas']]
            total = 0
            for red in redes:
                num_vis = Miembro.objects.filter(fechaAsignacionGAR__range = (fecha_i, fecha_f), grupo__red = red).count()
                values.append([str(red.nombre), num_vis])
                total = total + num_vis
                titulo = ''

            if 'type' in request.POST:
                if request.POST['type'] == '1':
                    tipo = 1
                else:
                    tipo = 2

            if 'reportePDF' in request.POST:
                values.append(['Total', total])
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(agenteAdminTest, login_url="/dont_have_permissions/")
def asignacionGAR(request):
    """Este reporte muestra el total de personas que han sido asignadas, que no les interesa, etc a un GAR en un rango de fechas
        escogidas por el usuario. Para este reporte se toman en cuenta los datos de las llamadas(pertenece, interesado, etc)."""

    tipo = 1
    titulo_pag = 'Control de asignacion a GAR'
    if request.method == 'POST':
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fecha_i = form.cleaned_data['fechai']
            fecha_f = form.cleaned_data['fechaf']
            opciones = {'fi': fecha_i, 'ff': fecha_f}
            sw = True

            values = [['Control', 'Miembros']]
            num_miembros = CambioTipo.objects.filter(fecha__range = (fecha_i, fecha_f), nuevoTipo__nombre__iexact = 'Visita').count()
            num_AsignadoGAR = CambioTipo.objects.filter(fecha__range = (fecha_i, fecha_f), nuevoTipo__nombre__iexact = 'Visita', miembro__asignadoGAR = True).count()
            num_asisteGAR = CambioTipo.objects.filter(fecha__range = (fecha_i, fecha_f), nuevoTipo__nombre__iexact = 'Visita', miembro__asisteGAR = True).count()
            num_noInteresadoGAR = CambioTipo.objects.filter(fecha__range = (fecha_i, fecha_f), nuevoTipo__nombre__iexact = 'Visita', miembro__noInteresadoGAR = True).count()
#            num_miembros = Miembro.objects.filter(fechaRegistro__range = (fecha_i, fecha_f)).count()
#            num_AsignadoGAR = Miembro.objects.filter(fechaRegistro__range = (fecha_i, fecha_f), asignadoGAR = True).count()
#            num_asisteGAR = Miembro.objects.filter(fechaRegistro__range = (fecha_i, fecha_f), asisteGAR = True).count()
#            num_noInteresadoGAR = Miembro.objects.filter(fechaRegistro__range = (fecha_i, fecha_f), noInteresadoGAR = True).count()
            num_noAsignadoGAR = num_miembros-num_AsignadoGAR-num_asisteGAR-num_noInteresadoGAR

            values.append(['Por asignar GAR', num_noAsignadoGAR])
            values.append(['Asignado GAR', num_AsignadoGAR])
            values.append(['Asiste GAR', num_asisteGAR])
            values.append(['No interesados GAR', num_noInteresadoGAR])
            total = num_miembros
            titulo = ''

            if 'type' in request.POST:
                if request.POST['type'] == '1':
                    tipo = 1
                else:
                    tipo = 2

            if 'reportePDF' in request.POST:
                values.append(['Total', total])
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(agenteAdminTest, login_url="/dont_have_permissions/")
def detalleLlamada(request, llamada):
    """Este reporte muestra el total de personas que se le hicieron llamadas de consolidacion en una fecha determinada."""

    tipo = 1
    if llamada==1:
        titulo_pag = 'Primera Llamada realizada en la iglesia'
    else:
        titulo_pag = 'Segunda Llamada realizada en la iglesia'
    if request.method == 'POST':
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fecha_i = form.cleaned_data['fechai']
            fecha_f = form.cleaned_data['fechaf']
            opciones = {'fi': fecha_i, 'ff': fecha_f}
            sw = True

            values = [['Detalles', 'Llamadas']]
            total  = 0
            detalles = DetalleLlamada.objects.all()
            for det in detalles:
                if llamada==1:
                    num = Miembro.objects.filter(fechaPrimeraLlamada__range = (fecha_i, fecha_f), detallePrimeraLlamada = det).count()
                else:
                    num = Miembro.objects.filter(fechaSegundaLlamada__range = (fecha_i, fecha_f), detalleSegundaLlamada = det).count()
                total = total + num
                values.append([str(det.nombre), num])
                titulo = ''

            if 'type' in request.POST:
                if request.POST['type'] == '1':
                    tipo = 1
                else:
                    tipo = 2

            if 'reportePDF' in request.POST:
                values.append(['Total', total])
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(agenteAdminTest, login_url="/dont_have_permissions/")
def visitasPorMes(request, por_red):
    """Este reporte muestra el total de visitas registradas por mes y el total de visitas de una red registradas por mes.
        El usuario debe escoger los meses los cuales se mostraran en el reporte."""

    tipo = 1
    if por_red:
        titulo_pag = 'Visitas asignadas a una red por mes'
    else:
        titulo_pag = 'Visitas registradas por mes'
    if request.method == 'POST':
        if por_red:
            form = FormularioVisitasRedPorMes(request.POST or None)
        else:
            form = FormularioVisitasPorMes(request.POST or None)
        if form.is_valid():
            ano = int(form.cleaned_data['ano'])
            meses = request.POST.getlist('meses')
            opciones = {'ano': ano}
            if por_red:
                red = Red.objects.get(id = form.cleaned_data['red'])
                opciones['red'] = red.nombre.capitalize()
            sw = True

            values = [['Meses', 'Visitas registradas']]
            total = 0
            for mes in meses:
                mes = int(mes)
                ult_dia_mes = calendar.monthrange(ano, mes)[1]
                fecha_i = datetime.date(ano, mes, 1)
                fecha_f = datetime.date(ano, mes, ult_dia_mes)
                if por_red:
                    num_vis = Miembro.objects.filter(fechaAsignacionGAR__range = (fecha_i, fecha_f), grupo__red = red).count()
                else:
                    num_vis = CambioTipo.objects.filter(fecha__range = (fecha_i, fecha_f), nuevoTipo__nombre__iexact = 'Visita').count()
                mes_nb = calendar.month_name[mes]
                total = total + num_vis
                values.append([mes_nb, num_vis])

            if 'type' in request.POST:
                if request.POST['type'] == '1':
                    tipo = 1
                else:
                    tipo = 2

            if 'reportePDF' in request.POST:
                values.append(['Total', total])
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        if por_red:
            form = FormularioVisitasRedPorMes()
        else:
            form = FormularioVisitasPorMes()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_mes.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def asistenciaGrupos(request):
    """Muestra la asistencia de los miembros de un grupo de amistad a las reuniones."""

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == 'POST':
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fechai = form.cleaned_data['fechai']
            fechaf = form.cleaned_data['fechaf']
            grupo_lidera = miembro.grupoLidera()

            if grupo_lidera is not None:
                reuniones = ReunionGAR.objects.filter(grupo=grupo_lidera, fecha__gt = fechai, fecha__lt = fechaf).order_by('fecha')
                miembros_grupo = grupo_lidera.miembrosGrupo().order_by('nombre', 'primerApellido')
                for m in miembros_grupo:
                    f = []
                    for r in reuniones:
                        try:
                            a = AsistenciaMiembro.objects.get(miembro=m, reunion=r)
                            asistio = a.asistencia
                        except :
                            asistio = False
                        f.append(asistio)
                    m.asis = f
    else:
        form = FormularioRangoFechas()

    return render_to_response('reportes/asistencia_grupos.html', locals(), context_instance=RequestContext(request))

def listaGruposDescendientes(miembro):
    """Devuelve una lista con todos los grupos descendientes del grupo del miembro usado como parametro para ser
        usada en un choice field."""
    
    grupo = miembro.grupoLidera()
    listaG = [grupo]
    discipulos = list(miembro.discipulos())
    while len(discipulos)>0:
        d = discipulos.pop(0)
        g = d.grupoLidera()
        if g:
            if g not in listaG:
                listaG.append(g)
            lid = Miembro.objects.filter(id__in = g.listaLideres())
            for l in lid: #Se elimina los otros lideres de la lista de discipulos para que no se repita el grupo.
                if l in discipulos:
                    discipulos.remove(l)
        if d.discipulos(): #Se agregan los discipulos del miembro en la lista de discipulos.
            discipulos.extend(list(d.discipulos()))
    return listaG

def listaCaminoGrupos(grupoi, grupof):
    """Devuelve los grupos que se encuentran en la camino del grupo inicial, al grupo final."""

    listaG = [grupof]
    if grupof != grupoi:
        m = Miembro.objects.get(id = grupof.listaLideres()[0])
        padre = m.grupo
        while padre != grupoi:
            if padre not in listaG:
                listaG.insert(0, padre)
            m = Miembro.objects.get(id = padre.listaLideres()[0])
            padre = m.grupo
        if padre not in listaG :
            listaG.insert(0, padre)
    return listaG

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def pasosPorMiembros(request):
    """Muestra los miembros de los grupos seleccionados y los pasos hechos por cada miembro."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)
    pasos = Pasos.objects.all().order_by('prioridad')
    descendientes = False

    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['id'])
            lider_i = Miembro.objects.get(id = grupo_i.listaLideres()[0])
            data = serializers.serialize('json', listaGruposDescendientes(lider_i))
            return HttpResponse(data, content_type="application/javascript")

        if 'verReporte' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
            if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                descendientes = True
                grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
            else:
                grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                grupos = listaCaminoGrupos(grupo_i, grupo_f)

            for g in grupos:
                miembros_grupo = g.miembrosGrupo().order_by('nombre', 'primerApellido')
                for m in miembros_grupo:
                    f = []
                    for p in pasos:
                        try:
                            c = CumplimientoPasos.objects.get(miembro=m, paso=p)
                            cumplio = True
                        except :
                            cumplio = False
                        f.append(cumplio)
                    m.cumple = f
                g.m_grupo = miembros_grupo

    return render_to_response('reportes/pasosPorMiembro.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def PasosTotales(request):
    """Muestra un reporte de pasos por totales."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)
    pasos = Pasos.objects.all().order_by('prioridad')
    descendientes = False
    sw = False

    tipo = 1
    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['id'])
            lider_i = Miembro.objects.get(id = grupo_i.listaLideres()[0])
            data = serializers.serialize('json', listaGruposDescendientes(lider_i))
            return HttpResponse(data, content_type="application/javascript")
        else:
            grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
            opciones = {'gi': grupo_i.nombre.capitalize()}
            sw = True

            if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                descendientes = True
                opciones['gf'] = 'Descendientes'
                grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
            else:
                grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                opciones['gf'] = grupo_f.nombre.capitalize()
                listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                grupos = listaCaminoGrupos(grupo_i, grupo_f)

            miembros = []
            for g in grupos:
                miembros.extend(g.miembrosGrupo())

            values = [['Pasos', 'Miembros']]
            total = len(miembros)
            for p in pasos:
                num_m = CumplimientoPasos.objects.filter(paso=p, miembro__in=miembros).count()
                values.append([str(p.nombre), num_m])

            m_cumplen = CumplimientoPasos.objects.filter(paso__in = pasos, miembro__in = miembros).values_list('miembro', flat=True)
            total_m = Miembro.objects.filter(id__in = m_cumplen).count()
            values.append(['No han realizado ningun paso', len(miembros)-total_m])

            if 'type' in request.POST:
                if request.POST['type'] == '1':
                    tipo = 1
                else:
                    tipo = 2
            
            if 'reportePDF' in request.POST:
                values.append(['Total', total])
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, 'Numero de miembros por pasos', opciones, values, tipo, True)
                return response
    
    return render_to_response('reportes/pasosTotales.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def PasosRangoFecha(request):
    """Muestra un reporte de pasos por un rango de fecha."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)
    pasos = Pasos.objects.all().order_by('prioridad')
    descendientes = False

    tipo = 1
    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['id'])
            lider_i = Miembro.objects.get(id = grupo_i.listaLideres()[0])
            data = serializers.serialize('json', listaGruposDescendientes(lider_i))
            return HttpResponse(data, content_type="application/javascript")
        else:
            form = FormularioRangoFechas(request.POST)
            if form.is_valid():
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
                opciones = {'fi': fechai, 'ff': fechaf, 'gi': grupo_i.nombre.capitalize()}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                    descendientes = True
                    opciones['gf'] = 'Descendientes'
                    grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                else:
                    grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                    opciones['gf'] = grupo_f.nombre.capitalize()
                    listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                    grupos = listaCaminoGrupos(grupo_i, grupo_f)

                miembros = []
                for g in grupos:
                    miembros.extend(g.miembrosGrupo())

                values = [['Pasos', 'Miembros']]
                total = 0
                for p in pasos:
                    num_m = CumplimientoPasos.objects.filter(paso=p, miembro__in=miembros, fecha__range = (fechai, fechaf)).count()
                    total = total + num_m
                    values.append([str(p.nombre), num_m])

                if 'type' in request.POST:
                    if request.POST['type'] == '1':
                        tipo = 1
                    else:
                        tipo = 2

                if 'reportePDF' in request.POST:
                    values.append(['Total', total])
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'
                    PdfTemplate(response, 'Numero de miembros por pasos en un rango de fecha', opciones, values, tipo, True)
                    return response
    else:
        form = FormularioRangoFechas()
        sw = False

    return render_to_response('reportes/pasosRangoFecha.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def estadisticoReunionesGar(request):
    """Muestra un estadistico de los reportes de reunion GAR segun los grupos, las opciones y el rango de fecha escogidos."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.all() #filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)

    descendientes = False
    ofrenda = False
    lid_asis = False
    visitas = False
    asis_reg = False

    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['id'])
            lider_i = Miembro.objects.get(id = grupo_i.listaLideres()[0])
            data = serializers.serialize('json', listaGruposDescendientes(lider_i))
            return HttpResponse(data, content_type="application/javascript")
        else:
            form = FormularioRangoFechas(request.POST or None)
            if form.is_valid():
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
                opciones = {'fi': fechai, 'ff': fechaf, 'gi': grupo_i.nombre.capitalize()}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                    descendientes = True
                    opciones['gf'] = 'Todos los descendientes'
                    grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                else:
                    grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                    opciones['gf'] = grupo_f.nombre.capitalize()
                    listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                    grupos = listaCaminoGrupos(grupo_i, grupo_f)

                total_grupos = len(grupos)
                total_grupos_inactivos = len([grupo for grupo in grupos if grupo.estado=='I'])
                opciones['total_grupos'] = total_grupos
                opciones['total_grupos_inactivos'] = total_grupos_inactivos
                sw_while = True

                if 'reportePDF' in request.POST:
                    values = [['Rango fecha', 'Visitas', 'Regulares', 'Lideres', 'Total asistentes', 'Grupos que reportaron sobres',
                               'Grupos que no han reportado sobres', 'Porcentaje de utilizacion']]

                    values_g = [['Rango fecha', 'Visitas', 'Regulares', 'lideres']]
                    while sw_while:
                        sig = fechai + datetime.timedelta(days = 6)

                        numPer = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'), Sum('numeroVisitas'), Sum('numeroTotalAsistentes'), Count('id'))
                        if numPer['numeroLideresAsistentes__sum'] is None:
                            sumLid = 0
                        else:
                            sumLid = numPer['numeroLideresAsistentes__sum']

                        if numPer['numeroVisitas__sum'] is None:
                            sumVis = 0
                        else:
                            sumVis = numPer['numeroVisitas__sum']

                        if numPer['numeroTotalAsistentes__sum'] is None:
                            sumTot = 0
                        else:
                            sumTot = numPer['numeroTotalAsistentes__sum']

                        numReg = sumTot-sumVis-sumLid

                        if numPer['id__count'] is None:
                            numSobres = 0
                        else:
                            numSobres = numPer['id__count']

                        numSobresNo = total_grupos - total_grupos_inactivos - numSobres
                        utillizacion = round(float(numSobres)/(total_grupos-total_grupos_inactivos)*100, 2)

                        l = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y"), sumVis, numReg, sumLid, sumTot, numSobres, numSobresNo, utillizacion]
                        lg = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y"), sumVis, numReg, sumLid]

                        values.append(l)
                        values_g.append(lg)

                        fechai = sig + datetime.timedelta(days = 1)
                        if sig >= fechaf:
                            sw_while = False

                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'
                    PdfTemplate(response, 'Estadistico de reuniones GAR', opciones, values_g, 3, tabla=values)
                    return response
                else:
                    values = [['Dates']]
                    while sw_while:
                        sig = fechai + datetime.timedelta(days = 6)

                        if 'ofrenda' in request.POST and request.POST['ofrenda']=='S':
                            ofrenda = True
                            if 'Ofrenda' not in values[0]:
                                values[0].append('Ofrenda')
                            sum_ofrenda = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('ofrenda'))
                            if sum_ofrenda['ofrenda__sum'] is None:
                                sum = 0
                            else:
                                sum = sum_ofrenda['ofrenda__sum']
                            values.append([fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y"), float(sum)])
                        else:
                            l = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y")]
                            if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                                lid_asis = True
                                if 'Numero de lideres asistentes' not in values[0]:
                                    values[0].append('Numero de lideres asistentes')
                                numlid = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                                if numlid['numeroLideresAsistentes__sum'] is None:
                                    sumLid = 0
                                else:
                                    sumLid = numlid['numeroLideresAsistentes__sum']
                                l.append(sumLid)
                            if 'visitas' in request.POST and request.POST['visitas']=='S':
                                visitas = True
                                if 'Numero de visitas' not in values[0]:
                                    values[0].append('Numero de visitas')
                                numVis = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroVisitas'))
                                if numVis['numeroVisitas__sum'] is None:
                                    sumVis = 0
                                else:
                                    sumVis = numVis['numeroVisitas__sum']
                                l.append(sumVis)
                            if 'asis_reg' in request.POST and request.POST['asis_reg']=='S':
                                asis_reg = True
                                if 'Numero de asistentes regulares' not in values[0]:
                                    values[0].append('Numero de asistentes regulares')
                                numPer = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'), Sum('numeroVisitas'), Sum('numeroTotalAsistentes'))

                                if numPer['numeroLideresAsistentes__sum'] is None:
                                    sumLid = 0
                                else:
                                    sumLid = numPer['numeroLideresAsistentes__sum']

                                if numPer['numeroVisitas__sum'] is None:
                                    sumVis = 0
                                else:
                                    sumVis = numPer['numeroVisitas__sum']

                                if numPer['numeroTotalAsistentes__sum'] is None:
                                    sumTot = 0
                                else:
                                    sumTot = numPer['numeroTotalAsistentes__sum']

                                numAsis = sumTot-sumVis-sumLid
                                l.append(numAsis)
                            values.append(l)
                        fechai = sig + datetime.timedelta(days = 1)
                        if sig >= fechaf:
                            sw_while = False
    else:
        form = FormularioRangoFechas()
        sw = False
    
    return render_to_response('reportes/estadistico_gar.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def estadisticoReunionesDiscipulado(request):
    """Muestra un estadistico de los reportes de reunion discipulado segun los grupos, las opciones y el rango de fecha escogidos."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)
    descendientes = False
    ofrenda = False
    lid_asis = False
    asis_reg = False #discipulos

    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['id'])
            lider_i = Miembro.objects.get(id = grupo_i.listaLideres()[0])
            data = serializers.serialize('json', listaGruposDescendientes(lider_i))
            return HttpResponse(data, content_type="application/javascript")
        else:
            form = FormularioPredicas(miembro=miembro, data=request.POST)
            if form.is_valid():
                predica = form.cleaned_data['predica']
                grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
                opciones = {'predica': predica.nombre.capitalize(), 'gi': grupo_i.nombre.capitalize()}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                    descendientes = True
                    opciones['gf'] = 'Descendientes'
                    grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                else:
                    grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                    opciones['gf'] = grupo_f.nombre.capitalize()
                    listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                    grupos = listaCaminoGrupos(grupo_i, grupo_f)

                values = [['Predica']]
                sw_while = True

                if 'ofrenda' in request.POST and request.POST['ofrenda']=='S':
                    ofrenda = True
                    if 'Ofrenda' not in values[0]:
                        values[0].append('Ofrenda')
                    sum_ofrenda = ReunionDiscipulado.objects.filter(predica = predica, grupo__in = grupos).aggregate(Sum('ofrenda'))
                    if sum_ofrenda['ofrenda__sum'] is None:
                        sum = 0
                    else:
                        sum = sum_ofrenda['ofrenda__sum']
                    values.append([str(predica), float(sum)])
                else:
                    l = [predica.nombre]
                    if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                        lid_asis = True
                        if 'Lideres asistentes' not in values[0]:
                            values[0].append('Lideres asistentes')
                        numlid = ReunionDiscipulado.objects.filter(predica = predica, grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                        if numlid['numeroLideresAsistentes__sum'] is None:
                            sumLid = 0
                        else:
                            sumLid = numlid['numeroLideresAsistentes__sum']
                        l.append(sumLid)
                    if 'asis_reg' in request.POST and request.POST['asis_reg']=='S':
                        asis_reg = True
                        if 'Asistentes regulares' not in values[0]:
                            values[0].append('Asistentes regulares')
                        # reg = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                        reg = ReunionDiscipulado.objects.filter(predica = predica, grupo__in = grupos)
                        numAsis = AsistenciaDiscipulado.objects.filter(reunion__in = reg, asistencia = True).count()
                        l.append(numAsis)
                    values.append(l)
                if 'reportePDF' in request.POST:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'
                    PdfTemplate(response, 'Estadistico de reuniones Discipulado', opciones, values, 2)
                    return response
    else:
        form = FormularioPredicas(miembro=miembro)
        sw = False

    return render_to_response('reportes/estadistico_discipulado.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def estadisticoTotalizadoReunionesGar(request):
    """Muestra un estadistico de los reportes de reunion GAR totalizado por discipulo segun el grupo, las opciones y el rango de fecha escogidos."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)
    ofrenda = False
    lid_asis = False
    visitas = False
    asis_reg = False

    if request.method == 'POST':
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fechai = form.cleaned_data['fechai']
            fechaf = form.cleaned_data['fechaf']
            grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
            discipulos = Miembro.objects.get(id = grupo_i.listaLideres()[0]).discipulos()
            grupoDis = Grupo.objects.filter(Q(lider1__in = discipulos) | Q(lider2__in = discipulos))
            opciones = {'fi': fechai, 'ff': fechaf, 'g': grupo_i.nombre.capitalize()}
            sw = True

            n = ['Dates']
            n.extend(["%s" % (nom.encode('ascii', 'ignore')) for nom in grupoDis.values_list('nombre', flat=True)])
            values = [n]
            sw_while = True
            while sw_while:
                sig = fechai + datetime.timedelta(days = 6)
                l = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y")]

                for g in grupoDis:
                    d = Miembro.objects.get(id = g.listaLideres()[0])
                    grupos = listaGruposDescendientes(d)

                    if 'ofrenda' in request.POST and request.POST['ofrenda']=='S':
                        ofrenda = True
                        opciones['opt'] = 'Ofrendas'
                        titulo = "'Ofrendas'"
                        sum_ofrenda = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('ofrenda'))
                        if sum_ofrenda['ofrenda__sum'] is None:
                            suma = 0
                        else:
                            suma = sum_ofrenda['ofrenda__sum']
                        l.append(float(suma))
                    else:
                        if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                            lid_asis = True
                            opciones['opt'] = 'Lideres Asistentes'
                            titulo = "'Lideres Asistentes'"
                            numlid = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                            if numlid['numeroLideresAsistentes__sum'] is None:
                                sumLid = 0
                            else:
                                sumLid = numlid['numeroLideresAsistentes__sum']
                            l.append(sumLid)
                        else:
                            if 'visitas' in request.POST and request.POST['visitas']=='S':
                                visitas = True
                                opciones['opt'] = 'Visitas'
                                titulo = "'Visitas'"
                                numVis = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroVisitas'))
                                if numVis['numeroVisitas__sum'] is None:
                                    sumVis = 0
                                else:
                                    sumVis = numVis['numeroVisitas__sum']
                                l.append(sumVis)
                            else:
                                if 'asis_reg' in request.POST and request.POST['asis_reg']=='S':
                                    asis_reg = True
                                    opciones['opt'] = 'Asistentes Regulares'
                                    titulo = "'Asistentes Regulares'"
                                    reg = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                                    numAsis = AsistenciaMiembro.objects.filter(reunion__in = reg, asistencia = True).count()
                                    l.append(numAsis)
                values.append(l)
                fechai = sig + datetime.timedelta(days=1)
                if sig >= fechaf:
                    sw_while = False

            if 'reportePDF' in request.POST:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, 'Estadistico de reuniones GAR totalizadas por discipulo', opciones, values, 2)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    return render_to_response('reportes/estadistico_total_gar.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def estadisticoTotalizadoReunionesDiscipulado(request):
    """Muestra un estadistico de los reportes de reunion discipulado totalizado por discipulo segun el grupo, las opciones y el rango de fecha escogidos."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        grupoP = Grupo.objects.get(red=None)
        liderP = Miembro.objects.get(id = grupoP.listaLideres()[0])
        #listaGrupo_i = listaGruposDescendientes(liderP)
        listaGrupo_i = Grupo.objects.filter(estado='A')
    else:
        listaGrupo_i = listaGruposDescendientes(miembro)
    ofrenda = False
    lid_asis = False
    asis_reg = False

    if request.method == 'POST':
        form = FormularioPredicas(miembro=miembro, data=request.POST)
        if form.is_valid():
            predica = form.cleaned_data['predica']
            grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
            discipulos = Miembro.objects.get(id = grupo_i.listaLideres()[0]).discipulos()
            grupoDis = Grupo.objects.filter(Q(lider1__in = discipulos) | Q(lider2__in = discipulos))
            opciones = {'predica': predica.nombre.capitalize(), 'gi': grupo_i.nombre.capitalize()}
            sw = True

            n = ['Predica']
            print(grupoDis.values_list('nombre', flat=True))
            n.extend(grupoDis.values_list('nombre', flat=True))
            values = [n]
            sw_while = True
            # while sw_while:
            #     sig = fechai + datetime.timedelta(days = 6)
            #     l = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y")]
            l = [predica.nombre.upper()]

            for g in grupoDis:
                d = Miembro.objects.get(id = g.listaLideres()[0])
                grupos = listaGruposDescendientes(d)

                if 'ofrenda' in request.POST and request.POST['ofrenda']=='S':
                    ofrenda = True
                    opciones['opt'] = 'Ofrendas'
                    titulo = "'Ofrendas'"
                    # sum_ofrenda = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('ofrenda'))
                    sum_ofrenda = ReunionDiscipulado.objects.filter(predica = predica, grupo__in = grupos).aggregate(Sum('ofrenda'))
                    if sum_ofrenda['ofrenda__sum'] is None:
                        suma = 0
                    else:
                        suma = sum_ofrenda['ofrenda__sum']
                    l.append(float(suma))
                else:
                    if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                        lid_asis = True
                        opciones['opt'] = 'Lideres Asistentes'
                        titulo = "'Lideres Asistentes'"
                        # numlid = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                        numlid = ReunionDiscipulado.objects.filter(predica = predica, grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                        if numlid['numeroLideresAsistentes__sum'] is None:
                            sumLid = 0
                        else:
                            sumLid = numlid['numeroLideresAsistentes__sum']
                        l.append(sumLid)
                    else:
                        if 'asis_reg' in request.POST and request.POST['asis_reg']=='S': #discipulos
                            asis_reg = True
                            opciones['opt'] = 'Asistentes Regulares'
                            titulo = "'Asistentes Regulares'"
                            # reg = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                            reg = ReunionDiscipulado.objects.filter(predica = predica, grupo__in = grupos)
                            numAsis = AsistenciaDiscipulado.objects.filter(reunion__in = reg, asistencia = True).count()
                            l.append(numAsis)
            values.append(l)
            # n.append(l)

            print('------------ ' + str(values))
            if 'reportePDF' in request.POST:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, 'Estadistico de reuniones Discipulado totalizadas por discipulo', opciones, values, 2)
                return response
    else:
        form = FormularioPredicas(miembro=miembro)
        sw = False

    return render_to_response('reportes/estadistico_total_discipulado.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def desarrolloGrupo(request):
    """Muestra un arbol de desarrollo de tu grupo."""

    miembro = Miembro.objects.get(usuario = request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        raiz = Grupo.objects.get(red = None)
        padre = Miembro.objects.get(id = raiz.listaLideres()[0])
    else:
        raiz = miembro.grupoLidera()
        padre = miembro
    pila = [[raiz]]
    act = None
    bajada = True
    discipulos = list(padre.discipulos())
    while len(discipulos)>0:
        #print 'dis:', discipulos
        d = discipulos.pop()
        hijo = d.grupoLidera()
        #print 'd:', d, 'hijo:', hijo
        if hijo:
            if act is not None:
                pila.append(act)
            sw = True
            while len(pila)>0 and sw:
                act = pila.pop()
                #print 'pila:', pila
                #print 'act:', act
                if act[len(act)-1]==d.grupo:
                    act.append([hijo])
                    bajada = True
                    sw = False
                elif act[len(act)-2]==d.grupo:
                    act[len(act)-1].append(hijo)
                    bajada = True
                    sw = False
                elif isinstance(act[-1], (tuple, list)) and bajada:
                    pila.append(act)
                    pila.append(act[len(act)-1])
                elif not isinstance(act[-1], (tuple, list)):
                    bajada = False
                #print '------------while pila------------'
            lid = Miembro.objects.filter(id__in = hijo.listaLideres())
            for l in lid: #Se elimina los otros lideres de la lista de discipulos para que no se repita el grupo.
                if l in discipulos:
                    discipulos.remove(l)
        if d.discipulos(): #Se agregan los discipulos del miembro en la lista de discipulos.
            discipulos.extend(list(d.discipulos()))
        #print '----------while disci-----------'
    #print 'act final:', act
    #print 'pila final:', pila
    if pila:
        arbol = pila[0]
    else:
        arbol = act
    return render_to_response('reportes/desarrollo_grupo.html', locals(), context_instance=RequestContext(request))

def listaGruposDescendientes_id(miembro):
    """Devuelve una lista con todos los ids de los grupos descendientes del grupo del miembro usado como parametro para ser
        usada en un choice field."""

    grupo = miembro.grupoLidera()
    listaG = [grupo.id]
    discipulos = list(miembro.discipulos())
    while len(discipulos)>0:
        d = discipulos.pop(0)
        g = d.grupoLidera()
        if g:
            if g not in listaG:
                listaG.append(g.id)
            lid = Miembro.objects.filter(id__in = g.listaLideres())
            for l in lid: #Se elimina los otros lideres de la lista de discipulos para que no se repita el grupo.
                if l in discipulos:
                    discipulos.remove(l)
        if d.discipulos(): #Se agregan los discipulos del miembro en la lista de discipulos.
            discipulos.extend(list(d.discipulos()))
    return listaG

isOk = False

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def ConsultarReportesSinEnviar(request, sobres=False):
    """Permite a un administrador y a un lider revisar que lideres no han registrado sus reportes de reuniones de grupo en un rango de fecha
        especificado. El usuario escoge el tipo de reunion, si la reunion es de GAR(1) o discipulado (2). Luego podra enviar un mail a los lideres
        que no han ingresado los reportes y a sus lideres. Para el lider solo muestra su arbol."""

    global isOk

    if isOk:
        messages.success(request,'Se han enviado los correros satisfactoriamente')
        isOk = False

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == 'POST':
        if 'Enviar' in request.POST and 'grupos_sin_reporte' in request.session:
            grupos = request.session['grupos_sin_reporte']
            sobres = request.session['sobres']

            from_mail = 'iglesia@mail.webfaction.com'
            mensaje = "Lideres de la iglesia,\n\n"
            if sobres: #Si es GAR y reporte de sobres
                asunto = 'Recordatorio entrega de ofrendas de reunion GAR'
                mensaje = mensaje + "Se les recuerda que no han entregado los sobres de las reuniones GAR de las siguientes fechas:\n\n"
            else: #Si es GAR y reporte reuniones
                asunto = 'Recordatorio ingreso de reportes de reunion GAR'
                mensaje = mensaje + "Se les recuerda que no han ingresado al sistema los reportes de las reuniones GAR de las siguientes fechas:\n\n"

            correos = []
            for ids,fechas in grupos.items():
                receptores = list()
                g = Grupo.objects.get(id=ids)
                mailLideres = Miembro.objects.filter(id__in=g.listaLideres()).values('email')
                receptores.extend(["%s" % (k['email']) for k in mailLideres])
                msj = mensaje + '\n'.join(map(str, fechas)) + "\n\nCordialmente,\n Admin"
                correos.append((asunto, msj, from_mail, receptores))
            print(tuple(correos))
            isOk = True

            sendMassMail(tuple(correos))
            return HttpResponseRedirect('/reportes/reportes_reuniones_sin_enviar/')

        form = FormularioReportesSinEnviar(request.POST)
        if 'verMorosos' in request.POST:
            if form.is_valid():
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupos = []
                gruposSinReporte = {}
                sw = True

                if miembro.usuario.has_perm("miembros.es_administrador"):
                    gr = Grupo.objects.filter(id__in = listaGruposDescendientes_id(Miembro.objects.get(id = Grupo.objects.get(red = None).listaLideres()[0])))
                else:
                    gr = Grupo.objects.filter(id__in = listaGruposDescendientes_id(miembro))

                while sw:
                    sig = fechai + datetime.timedelta(weeks = 1)

                    if sobres: #Entra si se escoge el reporte de entregas de sobres
                        gru = gr.filter(estado = 'A', fechaApertura__lt = sig).exclude(reuniongar__fecha__range = (fechai, sig), reuniongar__confirmacionentregaofrenda = True)
                    else: #Entra si se escoge el reporte de reuniones
                        gru = gr.filter(estado = 'A', fechaApertura__lt = sig).exclude(reuniongar__fecha__range = (fechai, sig))

                    for g in gru:
                        try:
                            i = grupos.index(g)
                            fecha = fechai + datetime.timedelta(days = int(g.diaGAR))
                            if fecha <= datetime.date.today():
                                grupos[i].fecha_reunion.append(fecha)
                                gruposSinReporte[g.id].append(str(fecha))
                        except:
                            # print(g.id)
                            fecha = fechai + datetime.timedelta(days = int(g.diaGAR))
                            if fecha <= datetime.date.today():
                                g.fecha_reunion = [fecha]
                                g.lideres = Miembro.objects.filter(id__in = g.listaLideres())
                                grupos.append(g)
                                strFecha = str(fecha)
                                gruposSinReporte[g.id] = [strFecha]

                    fechai = sig
                    if sig >= fechaf:
                        sw = False

                request.session['grupos_sin_reporte'] = gruposSinReporte
                request.session['sobres'] = sobres
    else:
        form = FormularioReportesSinEnviar()


    return render_to_response('reportes/morososGAR.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/dont_have_permissions/")
def ConsultarReportesDiscipuladoSinEnviar(request, sobres=False):
    """Permite a un administrador y a un lider revisar que lideres no han registrado sus reportes de reuniones de discipulado para una predica
        especificada. El usuario escoge la predica Luego podra enviar un mail a los lideres que no han ingresado los reportes y a sus lideres.
        Para el lider solo muestra su arbol."""

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == 'POST':
        if 'Enviar' in request.POST and 'grupos_sin_reporte' in request.session:
            grupos = request.session['grupos_sin_reporte']
            sobres = request.session['sobres']

            from_mail = 'iglesia@mail.webfaction.com'
            mensaje = "Lideres de la iglesia,\n\n"
            if sobres: #Si es reporte de sobres
                asunto = 'Recordatorio entrega de ofrendas de reunion discipulado'
                mensaje = mensaje + "Se les recuerda que no han entregado los sobres de las reuniones de discipulado de las siguientes fechas:\n\n"
            else: #Si es reporte reuniones
                asunto = 'Recordatorio ingreso de reportes de reunion discipulado'
                mensaje = mensaje + "Se les recuerda que no han ingresado al sistema los reportes de las reuniones de discipulado de las siguientes fechas:\n\n"

            correos = []
            for g in grupos:
                receptores = list()
                mailLideres = g.lideres.values('email')
                receptores.extend(["%s" % (k['email']) for k in mailLideres])
                msj = mensaje + '\n'.join(map(str, g.fecha_reunion)) + "\n\nCordialmente,\n Admin"
                correos.append((asunto, msj, from_mail, receptores))
            print(tuple(correos))

            sendMassMail(tuple(correos))

        form = FormularioPredicas(miembro, request.POST)
        if 'verMorosos' in request.POST:
            if form.is_valid():
                predica = form.cleaned_data['predica']
                sw = True

                if miembro.usuario.has_perm("miembros.es_administrador"):
                    gr = Grupo.objects.filter(id__in = listaGruposDescendientes_id(Miembro.objects.get(id = Grupo.objects.get(red = None).listaLideres()[0])))
                else:
                    gr = Grupo.objects.filter(id__in = listaGruposDescendientes_id(miembro))

                if sobres: #Entra si se escoge el reporte de entregas de sobres
                    grupos = gr.filter(estado = 'A').exclude(reuniondiscipulado__predica = predica, reuniondiscipulado__confirmacionentregaofrenda = True)
                else: #Entra si se escoge el reporte de reuniones
                    grupos = gr.filter(estado = 'A').exclude(reuniondiscipulado__predica = predica)

                for g in grupos:
                    g.lideres = Miembro.objects.filter(id__in = g.listaLideres())

                request.session['grupos_sin_reporte'] = grupos
                request.session['sobres'] = sobres
    else:
        form = FormularioPredicas(miembro)

    return render_to_response('reportes/morososDiscipulado.html', locals(), context_instance=RequestContext(request))


@user_passes_test(agenteAdminTest, login_url="/dont_have_permissions/")
def cumplimiento_llamadas_lideres_red(request):
    """Permite a un administrador y a un agente revisar el cumplimiento de las llamadas de los lideres de una red a las
    personas asignadas a su grupo dentro de un rango de fechas especificado."""

    grupos = []
    nadie = False
    if request.method == 'POST':
        form = FormularioCumplimientoLlamadasLideres(data=request.POST)

        if form.is_valid():
            grupos = form.obtener_grupos()
            if len(grupos) == 0:
                nadie = True
    else:
        form = FormularioCumplimientoLlamadasLideres()

    data = {'form': form, 'grupos': grupos, 'nadie':nadie}
    return render_to_response('reportes/llamadas_lideres_visitas.html', data, context_instance=RequestContext(request))


def sendMail(camposMail):
    subject = camposMail[0]
    mensaje = camposMail[1]
    receptor = camposMail[2]
    send_mail(subject, mensaje, 'iglesia@mail.webfaction.com', receptor, fail_silently=False)


def sendMassMail(correos):
    send_mass_mail(correos, fail_silently=False)
