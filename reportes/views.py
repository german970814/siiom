# Create your views here.
import calendar
from copy import copy
import datetime
from encodings.utf_8_sig import encode
from string import capitalize
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.mail import send_mail, send_mass_mail
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.datetime_safe import strftime
from grupos.models import Red, ReunionGAR, AsistenciaMiembro, Grupo, ReunionDiscipulado, AsistenciaDiscipulado
from miembros.models import Miembro, DetalleLlamada, Pasos, CumplimientoPasos, CambioTipo
from reportes.charts import PdfTemplate
from reportes.forms import FormularioRangoFechas, FormularioVisitasPorMes, FormularioVisitasRedPorMes, FormularioReportesSinEnviar

def liderAdminTest(user):
    return user.is_authenticated() \
            and (Group.objects.get(name__iexact = 'Lider') in user.groups.all() \
            or Group.objects.get(name__iexact = 'Administrador') in user.groups.all())

def agenteAdminTest(user):
    return user.is_authenticated() \
            and (Group.objects.get(name__iexact = 'Agente') in user.groups.all() \
            or Group.objects.get(name__iexact = 'Administrador') in user.groups.all())

@user_passes_test(agenteAdminTest, login_url="/iniciar_sesion/")
def visitasAsignadasRedes(request):
    """Este reporte muestra el total de visitas asignadas a las distintas redes en un rango de fechas escogida por el usuario."""

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
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(agenteAdminTest, login_url="/iniciar_sesion/")
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
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(agenteAdminTest, login_url="/iniciar_sesion/")
def detalleLlamada(request, llamada):
    """Este reporte muestra el total de personas que se le hicieron llamadas de consolidacion en una fecha determinada."""

    tipo = 1
    if llamada==1:
        titulo_pag = 'Primera lLamada realizada en la iglesia'
    else:
        titulo_pag = 'Segunda lLamada realizada en la iglesia'
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
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, titulo_pag, opciones, values, tipo, True)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('reportes/visitas_por_red.html', locals(), context_instance=RequestContext(request))

@user_passes_test(agenteAdminTest, login_url="/iniciar_sesion/")
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
            form = FormularioVisitasRedPorMes(request.POST)
        else:
            form = FormularioVisitasPorMes(request.POST)
        if form.is_valid():
            ano = int(form.cleaned_data['ano'])
            meses = request.POST.getlist('meses')
            opciones = {'ano': ano}
            if por_red:
                red = Red.objects.get(id = form.cleaned_data['red'])
                opciones['red'] = capitalize(red.nombre)
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
                response = HttpResponse(mimetype='application/pdf')
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

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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
            return HttpResponse(data, mimetype="application/javascript")

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

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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
            return HttpResponse(data, mimetype="application/javascript")
        else:
            grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
            opciones = {'gi': capitalize(grupo_i.nombre)}
            sw = True

            if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                descendientes = True
                opciones['gf'] = 'Descendientes'
                grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
            else:
                grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                opciones['gf'] = capitalize(grupo_f.nombre)
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
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, 'Numero de miembros por pasos', opciones, values, tipo, True)
                return response
    
    return render_to_response('reportes/pasosTotales.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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
            return HttpResponse(data, mimetype="application/javascript")
        else:
            form = FormularioRangoFechas(request.POST)
            if form.is_valid():
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
                opciones = {'fi': fechai, 'ff': fechaf, 'gi': capitalize(grupo_i.nombre)}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                    descendientes = True
                    opciones['gf'] = 'Descendientes'
                    grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                else:
                    grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                    opciones['gf'] = capitalize(grupo_f.nombre)
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
                print
                if 'type' in request.POST:
                    if request.POST['type'] == '1':
                        tipo = 1
                    else:
                        tipo = 2

                if 'reportePDF' in request.POST:
                    values.append(['Total', total])
                    response = HttpResponse(mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'
                    PdfTemplate(response, 'Numero de miembros por pasos en un rango de fecha', opciones, values, tipo, True)
                    return response
    else:
        form = FormularioRangoFechas()
        sw = False

    return render_to_response('reportes/pasosRangoFecha.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
def estadisticoReunionesGar(request):
    """Muestra un estadistico de los reportes de reunion GAR segun los grupos, las opciones y el rango de fecha escogidos."""

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
    visitas = False
    asis_reg = False

    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id = request.POST['id'])
            lider_i = Miembro.objects.get(id = grupo_i.listaLideres()[0])
            data = serializers.serialize('json', listaGruposDescendientes(lider_i))
            return HttpResponse(data, mimetype="application/javascript")
        else:
            form = FormularioRangoFechas(request.POST)
            if form.is_valid():
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
                opciones = {'fi': fechai, 'ff': fechaf, 'gi': capitalize(grupo_i.nombre)}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                    descendientes = True
                    opciones['gf'] = 'Descendientes'
                    grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                else:
                    grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                    opciones['gf'] = capitalize(grupo_f.nombre)
                    listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                    grupos = listaCaminoGrupos(grupo_i, grupo_f)

                values = [['Dates']]
                sw_while = True
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
                        values.append([fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y"), sum])
                    else:
                        l = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y")]
                        if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                            lid_asis = True
                            if 'Lideres asistentes' not in values[0]:
                                values[0].append('Lideres asistentes')
                            numlid = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                            if numlid['numeroLideresAsistentes__sum'] is None:
                                sumLid = 0
                            else:
                                sumLid = numlid['numeroLideresAsistentes__sum']
                            l.append(sumLid)
                        if 'visitas' in request.POST and request.POST['visitas']=='S':
                            visitas = True
                            if 'Visitas' not in values[0]:
                                values[0].append('Visitas')
                            numVis = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroVisitas'))
                            if numVis['numeroVisitas__sum'] is None:
                                sumVis = 0
                            else:
                                sumVis = numVis['numeroVisitas__sum']
                            l.append(sumVis)
                        if 'asis_reg' in request.POST and request.POST['asis_reg']=='S':
                            asis_reg = True
                            if 'Asistentes regulares' not in values[0]:
                                values[0].append('Asistentes regulares')
                            reg = ReunionGAR.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                            numAsis = AsistenciaMiembro.objects.filter(reunion__in = reg, asistencia = True).count()
                            l.append(numAsis)
                        values.append(l)
                    fechai = sig + datetime.timedelta(days = 1)
                    if sig >= fechaf:
                        sw_while = False
                if 'reportePDF' in request.POST:
                    response = HttpResponse(mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'
                    PdfTemplate(response, 'Estadistico de reuniones GAR', opciones, values, 3)
                    return response
    else:
        form = FormularioRangoFechas()
        sw = False
    
    return render_to_response('reportes/estadistico_gar.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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
            return HttpResponse(data, mimetype="application/javascript")
        else:
            form = FormularioRangoFechas(request.POST)
            if form.is_valid():
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
                opciones = {'fi': fechai, 'ff': fechaf, 'gi': capitalize(grupo_i.nombre)}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes']=='S':
                    descendientes = True
                    opciones['gf'] = 'Descendientes'
                    grupos = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                else:
                    grupo_f = Grupo.objects.get(id = request.POST['menuGrupo_f'])
                    opciones['gf'] = capitalize(grupo_f.nombre)
                    listaGrupo_f = listaGruposDescendientes(Miembro.objects.get(id = grupo_i.listaLideres()[0]))
                    grupos = listaCaminoGrupos(grupo_i, grupo_f)

                values = [['Dates']]
                sw_while = True
                while sw_while:
                    sig = fechai + datetime.timedelta(days = 6)

                    if 'ofrenda' in request.POST and request.POST['ofrenda']=='S':
                        ofrenda = True
                        if 'Ofrenda' not in values[0]:
                            values[0].append('Ofrenda')
                        sum_ofrenda = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('ofrenda'))
                        if sum_ofrenda['ofrenda__sum'] is None:
                            sum = 0
                        else:
                            sum = sum_ofrenda['ofrenda__sum']
                        values.append([fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y"), sum])
                    else:
                        l = [fechai.strftime("%d/%m/%y")+'-'+sig.strftime("%d/%m/%y")]
                        if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                            lid_asis = True
                            if 'Lideres asistentes' not in values[0]:
                                values[0].append('Lideres asistentes')
                            numlid = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
                            if numlid['numeroLideresAsistentes__sum'] is None:
                                sumLid = 0
                            else:
                                sumLid = numlid['numeroLideresAsistentes__sum']
                            l.append(sumLid)
                        if 'asis_reg' in request.POST and request.POST['asis_reg']=='S':
                            asis_reg = True
                            if 'Asistentes regulares' not in values[0]:
                                values[0].append('Asistentes regulares')
                            reg = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                            numAsis = AsistenciaDiscipulado.objects.filter(reunion__in = reg, asistencia = True).count()
                            l.append(numAsis)
                        values.append(l)
                    fechai = sig + datetime.timedelta(days=1)
                    if sig >= fechaf:
                        sw_while = False
                if 'reportePDF' in request.POST:
                    response = HttpResponse(mimetype='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'
                    PdfTemplate(response, 'Estadistico de reuniones Discipulado', opciones, values, 3)
                    return response
    else:
        form = FormularioRangoFechas()
        sw = False

    return render_to_response('reportes/estadistico_discipulado.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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
            opciones = {'fi': fechai, 'ff': fechaf, 'g': capitalize(grupo_i.nombre)}
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
                            sum = 0
                        else:
                            sum = sum_ofrenda['ofrenda__sum']
                        l.append(sum)
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
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, 'Estadistico de reuniones GAR totalizadas por discipulo', opciones, values, 2)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    return render_to_response('reportes/estadistico_total_gar.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fechai = form.cleaned_data['fechai']
            fechaf = form.cleaned_data['fechaf']
            grupo_i = Grupo.objects.get(id = request.POST['menuGrupo_i'])
            discipulos = Miembro.objects.get(id = grupo_i.listaLideres()[0]).discipulos()
            grupoDis = Grupo.objects.filter(Q(lider1__in = discipulos) | Q(lider2__in = discipulos))
            opciones = {'fi': fechai, 'ff': fechaf, 'g': capitalize(grupo_i.nombre)}
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
                        sum_ofrenda = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('ofrenda'))
                        if sum_ofrenda['ofrenda__sum'] is None:
                            sum = 0
                        else:
                            sum = sum_ofrenda['ofrenda__sum']
                        l.append(sum)
                    else:
                        if 'lid_asis' in request.POST and request.POST['lid_asis']=='S':
                            lid_asis = True
                            opciones['opt'] = 'Lideres Asistentes'
                            titulo = "'Lideres Asistentes'"
                            numlid = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos).aggregate(Sum('numeroLideresAsistentes'))
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
                                reg = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                                numAsis = AsistenciaDiscipulado.objects.filter(reunion__in = reg, asistencia = True).count()
                                l.append(numAsis)
                values.append(l)
                fechai = sig + datetime.timedelta(days=1)
                if sig >= fechaf:
                    sw_while = False

            if 'reportePDF' in request.POST:
                response = HttpResponse(mimetype='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=report.pdf'
                PdfTemplate(response, 'Estadistico de reuniones Discipulado totalizadas por discipulo', opciones, values, 2)
                return response
    else:
        form = FormularioRangoFechas()
        sw = False

    return render_to_response('reportes/estadistico_total_discipulado.html', locals(), context_instance=RequestContext(request))

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
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

@user_passes_test(liderAdminTest, login_url="/iniciar_sesion/")
def ConsultarReportesSinEnviar(request, sobres=False):
    """Permite a un administrador y a un lider revisar que lideres no han registrado sus reportes de reuniones de grupo en un rango de fecha
        especificado. El usuario escoge el tipo de reunion, si la reunion es de GAR(1) o discipulado (2). Luego podra enviar un mail a los lideres
        que no han ingresado los reportes y a sus lideres. Para el lider solo muestra su arbol."""

    miembro = Miembro.objects.get(usuario=request.user)
    if request.method == 'POST':
        if 'Enviar' in request.POST and 'grupos_sin_reporte' in request.session:
            grupos = request.session['grupos_sin_reporte']
            tipo_reunion = request.session['tipo_reporte']

            from_mail = 'iglesia@mail.webfaction.com'
            mensaje = "Lideres de la iglesia,\n\n"
            if tipo_reunion[0] and sobres: #Si es GAR y reporte de sobres
                asunto = 'Recordatorio entrega de ofrendas de reunion GAR'
                mensaje = mensaje + "Se les recuerda que no han entregado los sobres de las reuniones GAR de las siguientes fechas:\n\n"
            elif not tipo_reunion[0] and sobres: #Si es discipulado y reporte de sobres
                asunto = 'Recordatorio entrega de ofrendas de reunion discipulado'
                mensaje = mensaje + "Se les recuerda que no han entregado los sobres de las reuniones de discipulado de las siguientes fechas:\n\n"
            elif tipo_reunion[0] and not sobres: #Si es GAR y reporte reuniones
                asunto = 'Recordatorio ingreso de reportes de reunion GAR'
                mensaje = mensaje + "Se les recuerda que no han ingresado al sistema los reportes de las reuniones GAR de las siguientes fechas:\n\n"
            elif not tipo_reunion[0] and not sobres: #Si es discipulado y reporte reuniones
                asunto = 'Recordatorio ingreso de reportes de reunion discipulado'
                mensaje = mensaje + "Se les recuerda que no han ingresado al sistema los reportes de las reuniones de discipulado de las siguientes fechas:\n\n"

            correos = []
            for g in grupos:
                receptores = list()
                mailLideres = g.lideres.values('email')
                receptores.extend(["%s" % (k['email']) for k in mailLideres])
                msj = mensaje + '\n'.join(map(str, g.fecha_reunion)) + "\n\nCordialmente,\n Admin"
                correos.append((asunto, msj, from_mail, receptores))
            print tuple(correos)

            sendMassMail(tuple(correos))

        form = FormularioReportesSinEnviar(request.POST)
        if 'verMorosos' in request.POST:
            if form.is_valid():
                tipoReunion = form.cleaned_data['reunion']
                fechai = form.cleaned_data['fechai']
                fechaf = form.cleaned_data['fechaf']
                grupos = []
                sw = True

                if miembro.usuario.has_perm("miembros.es_administrador"):
                    gr = Grupo.objects.filter(id__in = listaGruposDescendientes_id(Miembro.objects.get(id = Grupo.objects.get(red = None).listaLideres()[0])))
                else:
                    gr = Grupo.objects.filter(id__in = listaGruposDescendientes_id(miembro))

                while sw:
                    sig = fechai + datetime.timedelta(weeks = 1)

                    if sobres: #Entra si se escoge el reporte de entregas de sobres
                        if tipoReunion == 1:
                            gru = gr.filter(estado = 'A').exclude(reuniongar__fecha__gte = fechai, reuniongar__fecha__lt = sig, reuniongar__confirmacionentregaofrenda = True)
                        else:
                            gru = gr.filter(estado = 'A').exclude(reuniondiscipulado__fecha__gte = fechai, reuniondiscipulado__fecha__lt = sig, reuniondiscipulado__confirmacionentregaofrenda = True)
                    else: #Entra si se escoge el reporte de reuniones
                        if tipoReunion == 1:
                            gru = gr.filter(estado = 'A').exclude(reuniongar__fecha__gte = fechai, reuniongar__fecha__lt = sig)
                        else:
                            gru = gr.filter(estado = 'A').exclude(reuniondiscipulado__fecha__gte = fechai, reuniondiscipulado__fecha__lt = sig)

                    for g in gru:
                        try:
                            i = grupos.index(g)
                            if tipoReunion == 1:
                                grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days = int(g.diaGAR)))
                            else:
                                grupos[i].fecha_reunion.append(fechai + datetime.timedelta(days = int(g.diaDiscipulado)))
                        except:
                            if tipoReunion == 1:
                                g.fecha_reunion = [fechai + datetime.timedelta(days = int(g.diaGAR))]
                            else:
                                g.fecha_reunion = [fechai + datetime.timedelta(days = int(g.diaDiscipulado))]
                            g.lideres = Miembro.objects.filter(id__in = g.listaLideres())
                            grupos.append(g)

                    fechai = sig
                    if sig >= fechaf:
                        sw = False

                request.session['grupos_sin_reporte'] = grupos
                request.session['tipo_reporte'] = [sobres, tipoReunion]
    else:
        form = FormularioReportesSinEnviar()

    return render_to_response('reportes/morososGAR.html', locals(), context_instance=RequestContext(request))

def sendMail(camposMail):
    subject = camposMail[0]
    mensaje = camposMail[1]
    receptor = camposMail[2]
    send_mail(subject, mensaje, 'iglesia@mail.webfaction.com', receptor, fail_silently = False)

def sendMassMail(correos):
    send_mass_mail(correos, fail_silently = False)



