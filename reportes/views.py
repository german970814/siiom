# Django imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, send_mass_mail
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

# Apps imports
from .charts import PdfTemplate
from .forms import (
    FormularioRangoFechas, FormularioPredicas,
    FormularioEstadisticoReunionesGAR, FormularioReportesSinConfirmar,
    TotalizadoReunionDiscipuladoForm
)
from .utils import fechas_reporte_generador
from common.decorators import permisos_requeridos
from grupos.utils import reunion_reportada
from grupos.models import ReunionGAR, Grupo, ReunionDiscipulado, AsistenciaDiscipulado
from miembros.models import Miembro

# Python Package
import datetime
import json
import copy


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_lider')
def estadistico_reuniones_discipulado(request):
    """Muestra un estadistico de los reportes de reunion discipulado segun los grupos,
    las opciones y el rango de fecha escogidos."""

    miembro = Miembro.objects.get(usuario=request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        listaGrupo_i = Grupo.objects.prefetch_related('lideres').all()  # ._suspendidos()  #.filter(estado='A')
    else:
        listaGrupo_i = Grupo.get_tree(miembro.grupo_lidera)
    descendientes = False
    ofrenda = False
    lid_asis = False
    asis_reg = False  # discipulos

    if request.method == 'POST':
        if 'combo' in request.POST:
            grupo_i = Grupo.objects.get(id=request.POST['id'])
            grupos = Grupo.get_tree(grupo_i)
            data = [{'pk': grupo.id, 'nombre': str(grupo)} for grupo in grupos]
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            form = FormularioPredicas(miembro=miembro, data=request.POST)
            if form.is_valid():
                predica = form.cleaned_data['predica']
                grupo_i = Grupo.objects.get(id=request.POST['menuGrupo_i'])
                opciones = {'predica': predica.nombre.capitalize(), 'gi': grupo_i.nombre.capitalize()}
                sw = True

                if 'descendientes' in request.POST and request.POST['descendientes'] == 'S':
                    descendientes = True
                    opciones['gf'] = 'Descendientes'
                    grupos = Grupo._get_tree(grupo_i)
                else:
                    grupo_f = Grupo.objects.get(id=request.POST['menuGrupo_f'])
                    opciones['gf'] = grupo_f.nombre.capitalize()
                    listaGrupo_f = grupo_i.grupos_red.prefetch_related('lideres')
                    grupos = Grupo.obtener_ruta(grupo_i, grupo_f)

                values = [['Predica']]
                sw_while = True

                if 'ofrenda' in request.POST and request.POST['ofrenda'] == 'S':
                    titulo = "'Ofrenda'"
                    ofrenda = True
                    if 'Ofrenda' not in values[0]:
                        values[0].append('Ofrenda')
                    sum_ofrenda = ReunionDiscipulado.objects.filter(predica=predica,
                                                                    grupo__in=grupos).aggregate(Sum('ofrenda'))
                    if sum_ofrenda['ofrenda__sum'] is None:
                        sum = 0
                    else:
                        sum = sum_ofrenda['ofrenda__sum']
                    values.append([str(predica), float(sum)])
                else:
                    l = [predica.nombre]
                    if 'lid_asis' in request.POST and request.POST['lid_asis'] == 'S':
                        titulo = "'Lideres Asistentes'"
                        lid_asis = True
                        if 'Lideres asistentes' not in values[0]:
                            values[0].append('Lideres asistentes')
                        numlid = ReunionDiscipulado.objects.filter(predica=predica,
                                                                   grupo__in=grupos).aggregate(
                                                                       Sum('numeroLideresAsistentes'))
                        if numlid['numeroLideresAsistentes__sum'] is None:
                            sumLid = 0
                        else:
                            sumLid = numlid['numeroLideresAsistentes__sum']
                        l.append(sumLid)
                    if 'asis_reg' in request.POST and request.POST['asis_reg'] == 'S':
                        titulo = "'Asistentes Regulares'"
                        asis_reg = True
                        if 'Asistentes regulares' not in values[0]:
                            values[0].append('Asistentes regulares')
                        # reg = ReunionDiscipulado.objects.filter(fecha__range = (fechai, sig), grupo__in = grupos)
                        reg = ReunionDiscipulado.objects.filter(predica=predica, grupo__in=grupos)
                        numAsis = AsistenciaDiscipulado.objects.filter(reunion__in=reg, asistencia=True).count()
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

    return render(request, 'reportes/estadistico_discipulado.html', locals())


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_lider')
def estadistico_totalizado_reuniones_gar(request):
    """Muestra un estadistico de los reportes de reunion GAR totalizado
    por discipulo segun el grupo, las opciones y el rango de fecha escogidos."""

    miembro = Miembro.objects.get(usuario=request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        listaGrupo_i = Grupo.objects.prefetch_related('lideres').all()
    else:
        listaGrupo_i = miembro.grupo_lidera.grupos_red.prefetch_related('lideres')
    ofrenda = False
    lid_asis = False
    visitas = False
    asis_reg = False

    if request.method == 'POST':
        form = FormularioRangoFechas(request.POST)
        if form.is_valid():
            fechai = form.cleaned_data['fechai']
            fechaf = form.cleaned_data['fechaf']
            grupo_i = Grupo.objects.get(id=request.POST['menuGrupo_i'])
            grupoDis = grupo_i.get_children()
            lista_redes = [Grupo.get_tree(grupo) for grupo in grupoDis]
            opciones = {'fi': fechai, 'ff': fechaf, 'g': grupo_i.nombre.capitalize()}
            sw = True

            n = ['Dates']
            n.extend(["%s" % nom for nom in grupoDis.values_list('nombre', flat=True)])
            values = [n]
            sw_while = True
            while sw_while:
                sig = fechai + datetime.timedelta(days=6)
                l = [fechai.strftime("%d/%m/%y") + '-' + sig.strftime("%d/%m/%y")]

                for grupos in lista_redes:

                    if 'opcion' in request.POST and request.POST['opcion'] == 'O':
                        ofrenda = True
                        opciones['opt'] = 'Ofrendas'
                        titulo = "'Ofrendas'"
                        sum_ofrenda = ReunionGAR.objects.filter(fecha__range=(fechai, sig),
                                                                grupo__in=grupos).aggregate(Sum('ofrenda'))
                        if sum_ofrenda['ofrenda__sum'] is None:
                            suma = 0
                        else:
                            suma = sum_ofrenda['ofrenda__sum']
                        l.append(float(suma))
                    else:
                        if 'opcion' in request.POST and request.POST['opcion'] == 'L':
                            lid_asis = True
                            opciones['opt'] = 'Lideres Asistentes'
                            titulo = "'Lideres Asistentes'"
                            numlid = ReunionGAR.objects.filter(fecha__range=(fechai, sig),
                                                               grupo__in=grupos).aggregate(
                                                                   Sum('numeroLideresAsistentes'))
                            if numlid['numeroLideresAsistentes__sum'] is None:
                                sumLid = 0
                            else:
                                sumLid = numlid['numeroLideresAsistentes__sum']
                            l.append(sumLid)
                        else:
                            if 'opcion' in request.POST and request.POST['opcion'] == 'V':
                                visitas = True
                                opciones['opt'] = 'Visitas'
                                titulo = "'Visitas'"
                                numVis = ReunionGAR.objects.filter(fecha__range=(fechai, sig),
                                                                   grupo__in=grupos).aggregate(Sum('numeroVisitas'))
                                if numVis['numeroVisitas__sum'] is None:
                                    sumVis = 0
                                else:
                                    sumVis = numVis['numeroVisitas__sum']
                                l.append(sumVis)
                            else:
                                if 'opcion' in request.POST and request.POST['opcion'] == 'A':
                                    asis_reg = True
                                    opciones['opt'] = 'Asistentes Regulares'
                                    titulo = "'Asistentes Regulares'"
                                    reg = ReunionGAR.objects.filter(fecha__range=(fechai, sig), grupo__in=grupos)
                                    numAsis = 0
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

    return render(request, 'reportes/estadistico_total_gar.html', locals())


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_lider')
def estadistico_totalizado_reuniones_discipulado(request):
    """Muestra un estadistico de los reportes de reunion discipulado
    totalizado por discipulo segun el grupo, las opciones y el rango de fecha escogidos."""

    # miembro = Miembro.objects.get(usuario=request.user)
    miembro = request.miembro
    if miembro.discipulos() or miembro.usuario.has_perm("miembros.es_administrador"):
        if request.method == 'POST':
            form = TotalizadoReunionDiscipuladoForm(request.miembro, data=request.POST)

            if form.is_valid():
                sw = True
                opciones, values, titulo, tiene_discipulos = form.obtener_totalizado()

                # se agrega un condicional que indique que l (la cual es la lista que contiene los valores)
                # de las respuestas de acuerdo a cada opcion, siempre y cuenta esta lista tenga mas dee un
                # valor, se puede hacer el reporte, de otro modo llegan campos vacios al PdfTemplate y lanza un error
                if 'reportePDF' in request.POST and len(values[1]) > 1:
                # if 'reportePDF' in request.POST and len(l) > 1:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=report.pdf'

                    PdfTemplate(response,
                                'Estadistico de reuniones Discipulado totalizadas por discipulo',
                                opciones, values, 2)
                    return response
        else:
            form = TotalizadoReunionDiscipuladoForm(request.miembro)
            sw = False

    return render(request, 'reportes/estadistico_total_discipulado.html', locals())


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_lider')
def estadistico_reuniones_gar(request):
    """
    Muestra un estadistico de los reportes de reunion GAR segun los grupos,
    las opciones y el rango de fecha escogidos.
    """

    # se obtiene el miembro
    miembro = Miembro.objects.get(usuario=request.user)

    # se crean los datos iniciales
    data = {}

    # si el usuario es administrador, tendrá una lista con todos los grupos
    if request.user.has_perm("miembros.es_administrador"):
        queryset_grupo = Grupo.objects.prefetch_related('lideres').all()
    else:
        # si no es administrador, solo puede ver los grupos debajo de el
        queryset_grupo = miembro.grupo_lidera.grupos_red.prefetch_related('lideres')

    # si el metodo es POST
    if request.method == 'POST':
        # se crea un formulario, con el queryset que irá en el campo de grupo
        form = FormularioEstadisticoReunionesGAR(data=request.POST, queryset_grupo=queryset_grupo)

        # si es valido formulario
        if form.is_valid():
            # se sacan los datos iniciales
            _fecha_inicial = form.cleaned_data['fecha_inicial']
            fecha_inicial = copy.deepcopy(_fecha_inicial)
            _fecha_final = form.cleaned_data['fecha_final']
            fecha_final = copy.deepcopy(_fecha_final)
            grupo = form.cleaned_data['grupo']
            descendientes = form.cleaned_data.get('descendientes', False)
            ofrenda = form.cleaned_data.get('ofrenda', False)

            # constants
            format_date = "%d/%m/%y"
            date_split = ' - '

            # helpers
            _helper = []
            labels_fecha = []
            values_porcentaje_utilidad = [labels_fecha, []]
            values_asistencias = [['Fechas']]
            morosos = []
            _morosos = {}
            data_table = []
            ofrendas = []

            # se empacan los datos a la vista
            data['values_porcentaje_utilidad'] = values_porcentaje_utilidad
            data['values_asistencias'] = values_asistencias

            # si hay descendientes en el formulario
            if descendientes:
                grupos = grupo._grupos_red.prefetch_related('lideres').only('fechaApertura', 'id', 'estado')
            else:
                grupos = Grupo._objects.filter(id=grupo.id)

            total_grupos_inactivos = grupos.inactivos().count()

            for fecha_inicial, fecha_final in fechas_reporte_generador(_fecha_inicial, _fecha_final):
                # esto, trae los que estuvieron activos antes de la fecha filtrada
                _grupos_semana = grupos.filter(historiales__fecha__lte=fecha_final).activos()  # .exclude(id=grupo.id)

                grupos_semana = _grupos_semana.count()

                # se sacan las reuniones que han ocurrido en la semana actual de el ciclo
                _reuniones = ReunionGAR.objects.filter(
                    fecha__range=(fecha_inicial, fecha_final),
                    grupo__in=_grupos_semana  # solo busca los reportes de los grupos de la semana
                ).defer(
                    'confirmacionEntregaOfrenda', 'novedades', 'predica'
                ).distinct()

                # se hacen las agregaciones, con los datos de los estadisticos por semana
                reuniones = _reuniones.aggregate(
                    lideres_asistentes=Sum('numeroLideresAsistentes'),
                    visitas_=Sum('numeroVisitas'),
                    total_asistentes=Sum('numeroTotalAsistentes'),
                    grupos_reportaron=Count('grupo', distinct=True)
                )

                # Si las agregaciones estan vacias, se pasan a 0 para evitar errores en las operaciones
                for key in reuniones:
                    if reuniones[key] is None:
                        reuniones[key] = 0

                # se agrega una nueva llave a las reuniones, con los asistentes regulares esa semana
                reuniones['asistentes_regulares'] = (
                    reuniones['total_asistentes'] - reuniones['visitas_'] -
                    reuniones['lideres_asistentes']
                )

                # se añaden las fechas
                fechas_str = fecha_inicial.strftime(format_date) + date_split + fecha_final.strftime(format_date)
                labels_fecha.insert(len(labels_fecha), fechas_str)  # se agrega como pila

                # si hay ofrendas
                if ofrenda:
                    # se crea por aparte el agregate de ofrendas
                    ofrenda_aggregate = _reuniones.aggregate(
                        ofrendas=Sum('ofrenda')
                    )
                    # se agrega de la forma [['fecha', ofrenda]]
                    if ofrenda_aggregate['ofrendas'] is None:
                        ofrenda_aggregate['ofrendas'] = 0
                    ofrendas.append([fechas_str, float(ofrenda_aggregate['ofrendas']) or 0])

                # se sacan los grupos sin reportar, vendria de la resta de los grupos de la semana, menos los sobres
                _sin_reportar = _grupos_semana.exclude(
                    id__in=_reuniones.values_list('grupo__id', flat=True)
                )
                # se saca el conteo de los grupos sin reportar
                sin_reportar = _sin_reportar.count()

                # se añaden los datos a el diccionario, para la tabla
                data_table.append(
                    {
                        'reuniones': reuniones,
                        'grupos_semana': grupos_semana,
                        'sin_reportar': sin_reportar,
                        'fecha': fechas_str
                    }
                )

                # se agregan a la lista de morosos
                if sin_reportar > 0:
                    _morosos_list_id = _sin_reportar.values_list('id', flat=True)
                    for x in _morosos_list_id:
                        if x.__str__() not in _morosos:
                            _morosos[x.__str__()] = [fechas_str]
                        else:
                            _morosos[x.__str__()].append(fechas_str)

                # porcentaje grupos que estan reportando
                grupos_reportaron = reuniones.pop('grupos_reportaron', 0)

                try:
                    # se intenta sacar el porcentaje, si grupos semana es 0, entonces no hay porcentaje
                    porcentaje_grupos_reportando = round(float(grupos_reportaron) / grupos_semana * 100, 2)
                except ZeroDivisionError:
                    porcentaje_grupos_reportando = 0

                # empaquetado de datos para porcetaje de utilidad
                values_porcentaje_utilidad[1].insert(len(values_porcentaje_utilidad[1]), porcentaje_grupos_reportando)
                # porcentaje quedaria de la forma
                # [['fecha1', 'fecha2'], [80, 30]]
                # se empaca el porcentaje a data_table, no puede llegar la lista vacia
                data_table[len(data_table) - 1]['porcentaje'] = porcentaje_grupos_reportando

                # empaquetado de datos para asistencias
                _auxiliar = []
                # se intenta organizar los datos de la mejor forma
                for key, item in reuniones.items():
                    # se reemplazan los '_' por espacios
                    key_to_word = key.replace('_', ' ').title()
                    if key_to_word not in values_asistencias[0]:
                        values_asistencias[0].insert(len(values_asistencias[0]), key_to_word)
                    # se agregan los valores a la variable auxiliar
                    # _auxiliar.append()
                    _auxiliar.insert(len(_auxiliar), [item, item.__str__()])  # [[1,1],[2,2],[3,3],[4,4]]
                _helper.insert(len(_helper), _auxiliar)  # [[[1,1],[2,2],[3,3],[4,4]], [[1,1],[2,2],[3,3],[4,4]]]

                # Para las barras de google, los datos deben quedar organizados de la forma
                # arr = [['Fecha', 'CAMPO1', 'CAMPO2'], ['Fecha', value1, 'value1', value2, 'value2']]

            # Grafico porcentaje Grupos Reportados
            for x, label in enumerate(labels_fecha):  # labels fecha contiene el tamaño de objetos base (No. semanas)
                # se agrega el label como iniacial para los valores de asistencia
                _lista = [label]
                for y, value in enumerate(_helper[x]):
                    # se agrega cada elemento de la lista en el orden correspondiente
                    _lista.append(_helper[x][y][0])
                    _lista.append(_helper[x][y][1])
                # se agrega a el array principal
                values_asistencias.append(_lista)

            morosos = list(Grupo._objects.filter(id__in=[x for x in _morosos]))

            for moroso in reversed(morosos):
                for fecha in _morosos[moroso.id.__str__()]:
                    _fecha = fecha.split(date_split)[0]
                    _fecha = datetime.datetime.strptime(_fecha, format_date)
                    if reunion_reportada(_fecha, moroso):
                        _morosos[moroso.id.__str__()].pop(_morosos[moroso.id.__str__()].index(fecha))
                if len(_morosos[moroso.id.__str__()]):
                    moroso.fechas = '; '.join(_morosos[moroso.id.__str__()])
                    moroso.no_reportes = len(_morosos[moroso.id.__str__()])
                else:
                    morosos.pop(morosos.index(moroso))

            data['sin_reportar'] = morosos
            data['tabla'] = data_table
            data['grafico'] = True
            data['values_ofrenda'] = ofrendas or None
            data['grupos_inactivos'] = total_grupos_inactivos

        else:
            # se envia el mensaje de error
            messages.error(request, _("Ha ocurrido un error en el formulario, verifica los campos"))
    else:
        form = FormularioEstadisticoReunionesGAR(queryset_grupo=queryset_grupo, initial={'descendientes': True})

    data['form'] = form
    data['miembro'] = miembro  # se agrega miembro a la data para el template

    return render(request, 'reportes/estadistico_gar.html', data)


@login_required
@permisos_requeridos('miembros.es_administrador', 'miembros.es_lider')
def confirmar_ofrenda_grupos_red(request):
    """Vista para confirmar la ofrenda de los grupos de acuerdo a un grupo inicial"""

    data = {}
    miembro = Miembro.objects.get(usuario=request.user)
    if miembro.usuario.has_perm('miembros.es_administrador'):
        queryset = Grupo.objects.prefetch_related('lideres').all().distinct()
    else:
        queryset = miembro.grupo_lidera.grupos_red.prefetch_related('lideres')

    if request.method == 'POST':
        if 'confirmar' in request.POST:
            data = {}
            try:
                reunion = ReunionGAR.objects.get(id=request.POST.get('confirmar'))
                reunion.confirmacionEntregaOfrenda = True
                reunion.save()
                data['response_code'] = 200
                data['message'] = 'Reporte confirmado exitosamente'
            except ReunionGAR.DoesNotExist:
                data['response_code'] = 400
                data['message'] = 'Lo sentimos pero no se ha podido confirmar el reporte'

            return HttpResponse(json.dumps(data), content_type='application/json')

        form = FormularioReportesSinConfirmar(data=request.POST, queryset=queryset)

        if form.is_valid():
            grupo = form.cleaned_data['grupo']
            fecha_inicial = form.cleaned_data['fecha_inicial']
            fecha_final = form.cleaned_data['fecha_final']
            descendientes = form.cleaned_data['descendientes']

            fecha_final += datetime.timedelta(days=1)

            if descendientes:
                grupos = grupo._grupos_red.prefetch_related('lideres').only('fechaApertura', 'id', 'estado')
            else:
                grupos = Grupo._objects.filter(id=grupo.id)

            reuniones = ReunionGAR.objects.filter(
                grupo__id__in=grupos.values_list('id', flat=True),
                fecha__range=(fecha_inicial, fecha_final),
                confirmacionEntregaOfrenda=False
            ).order_by('-fecha')

            data['reuniones'] = reuniones
            if len(reuniones) == 0:
                data['vacio'] = True

    else:
        form = FormularioReportesSinConfirmar(queryset=queryset)

    data['form'] = form

    return render(request, 'reportes/confirmar_ofrenda_grupos_red.html', data)
