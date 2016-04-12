# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from miembros.models import Miembro, CumplimientoPasos
from academia.models import Curso, Matricula, AsistenciaSesiones, Modulo,\
    Sesion, Reporte
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core import serializers
import datetime
from django.db.models.aggregates import Sum
from django.db.models import Q
from academia.forms import FormularioEvaluarModulo,\
    FormularioPromoverModulo, FormularioCrearCurso, FormularioEditarCurso,\
    FormularioMatricula, FormularioCrearModulo, FormularioCrearSesion,\
    FormularioRecibirPago


def eliminar(request, modelo, lista):
    ok = 0  # No hay nada en la lista
    if lista:
        ok = 1  # Los borro todos
        for e in lista:
            try:
                modelo.objects.get(id=e).delete()
            except ValueError as e:
                print(e)
                pass
            except:
                ok = 2  # Hubo un Error
    if ok == 1:
        messages.success(request, "Se ha eliminado correctamente")
    return ok


def maestroTest(user):
    return user.is_authenticated() \
           and Group.objects.get(name__iexact='Maestro') in user.groups.all()


def receptorTest(user):
    return  user.is_authenticated() \
            and Group.objects.get(name__iexact='Receptor') in user.groups.all()


def adminTest(user):
    return user.is_authenticated() \
           and Group.objects.get(name__iexact='Administrador') in user.groups.all()


def adminMaestroTest(user):
    return user.is_authenticated() \
           and (Group.objects.get(name__iexact = 'Administrador') in user.groups.all() \
                or Group.objects.get(name__iexact = 'Maestro') in user.groups.all())


#  -------------------------AMBOS----------------------------------
@user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
def verCursos(request, admin):
    """Permite a un maestro o a un administrador listar cursos."""
    miembro = Miembro.objects.get(usuario=request.user)
    if miembro.usuario.has_perm("miembros.es_administrador"):
        admin = True
    else:
        admin = False

    if request.method == 'POST':
        request.session['seleccionados'] = request.POST.getlist('seleccionados')
        if admin:
            return HttpResponseRedirect('/academia/admin_editar_curso/')
        else:
            return HttpResponseRedirect("/academia/editar_curso/")

    miembro = Miembro.objects.get(usuario=request.user)
    if admin:
        cursos = Curso.objects.all().order_by('estado', 'profesor__nombre')
        request.session['admin'] = True
    else:
        cursos = Curso.objects.filter(profesor=miembro, estado='A')
        request.session['admin'] = False
    return render_to_response("Academia/listar_cursos.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
def verDetalleCurso(request, curso):
    """Permite a un maestro o administrador ver los modulos y sesiones que se dan en un curso."""

    miembro = Miembro.objects.get(usuario=request.user)
    iid = int(curso)
    curso = Curso.objects.get(id=iid)
    modulos = curso.modulos.all()
    for modulo in modulos:
        modulo.sesiones = Sesion.objects.filter(modulo=modulo)
    return render_to_response("Academia/curso_detalle.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
def editarCurso(request, admin, url, pk, template_name="Academia/crear_curso.html"):
    """Permite a un maestro o administrador editar un cursos."""
    accion = 'Editar'
    curso = get_object_or_404(Curso, pk=pk)

    if request.method == 'POST':
        if admin:
            form = FormularioCrearCurso(request.POST or None, instance=curso)
        else:
            form = FormularioEditarCurso(request.POST or None, instance=curso)

        if form.is_valid():
            form.save()
            if admin:
                return HttpResponseRedirect("/academia/listar_cursos")
            else:
                return HttpResponseRedirect("/academia/cursos/")
    else:
        if admin:
            form = FormularioCrearCurso(instance=curso)
        else:
            form = FormularioEditarCurso(instance=curso)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
def listarEstudiantes(request, curso):
    """Permite listar los modulos dados en un curso y los estudiantes que asisten a dicho curso."""

    if request.method == 'POST':
        if 'Eliminar' in request.POST:
            eliminar(request, Matricula, request.POST.getlist('seleccionados'))
        else:
            seleccionados = list()
            for x in request.POST.getlist('seleccionados'):
                if isinstance(x, int):
                    if not x in seleccionados:
                        seleccionados.append(x)
                else:
                    try:
                        if not x in seleccionados:
                            seleccionados.append(int(x))
                    except ValueError:
                        pass
            sel = []
            [sel.append(y) for y in seleccionados if y not in sel]
            request.session['seleccionados'] = sel  # request.POST.getlist('seleccionados')
            request.session['curso'] = request.POST['curso']
            if request.POST['accion'] == 'M':
                return HttpResponseRedirect("/academia/evaluar_modulo/")
            if request.POST['accion'] == 'P':
                return HttpResponseRedirect("/academia/promover_estudiante/")

    # admin = request.session['admin']
    miembro = Miembro.objects.get(usuario=request.user)
    id = int(curso)
    curso = Curso.objects.get(id=id)
    mLanzados = CumplimientoPasos.objects.filter(paso__nombre__iexact='lanzamiento').values('miembro')
    estudiantes = Matricula.objects.filter(curso=curso).exclude(estudiante__id__in=mLanzados)
    for est in estudiantes:
        totalSesiones = Sesion.objects.filter(modulo=est.moduloActual).count()
        est.sesionesDadas = AsistenciaSesiones.objects.filter(matricula=est, sesion__modulo=est.moduloActual).count()
        est.sesionesFaltantes = totalSesiones - est.sesionesDadas
    return render_to_response("Academia/listar_estudiantes.html", locals(), context_instance=RequestContext(request))


@user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
def verDetalleEstudiante(request, est):
    """Permite ver la informacion del estudiante. Las sesiones dadas, su nota definitiva, etc."""

    miembro = Miembro.objects.get(usuario=request.user)
    id = int(est)
    try:
        est = Matricula.objects.get(id=id)
    except Matricula.DoesNotExist:
        raise Http404
    est.modulosDados = list(est.modulos.all())
    if est.moduloActual not in est.modulosDados and est.moduloActual is not None:
        est.modulosDados.append(est.moduloActual)
    for modulo in est.modulosDados:
        try:
            modulo.reporte = Reporte.objects.get(matricula=est, modulo=modulo)
        except:
            pass
        modulo.sesiones = Sesion.objects.filter(modulo=modulo)
        for sesion in modulo.sesiones:
            try:
                sesion.asistencia = AsistenciaSesiones.objects.get(matricula=est, sesion=sesion)
            except:
                pass
    return render_to_response("Academia/estudiante_detalle.html", locals(), context_instance=RequestContext(request))


#  ----------------------------------MAESTRO--------------------------------------
@user_passes_test(maestroTest, login_url="/dont_have_permissions/")
def maestroAsistencia(request):
    """ Permite a un maestro llenar la asistencia de una sesion. Se muestran los estudiantes que esten en dicho modulo
        o que el moduloActual sea None."""

    if request.method == 'POST':
        if 'combo' in request.POST:
            if request.POST['combo'] == 'idCurso':
                curso = Curso.objects.get(id=request.POST['id'])
                modulos = curso.modulos.all()
                data = serializers.serialize('json', modulos)
            else:
                modulo = Modulo.objects.get(id=request.POST['id'])
                sesiones = Sesion.objects.filter(modulo=modulo)
                data = serializers.serialize('json', sesiones)
            return HttpResponse(data, content_type="application/javascript")

        if 'verEstudiantes' in request.POST or 'aceptarAsistencia' in request.POST:
            try:
                c = request.POST.getlist('menuCursos')[0]
                m = request.POST.getlist('menuModulos')[0]
                s = request.POST.getlist('menuSesiones')[0]

                curso = Curso.objects.get(id=c)
                modulo = Modulo.objects.get(id=m)
                sesion = Sesion.objects.get(id=s)
                modulos = curso.modulos.all()
                sesiones = Sesion.objects.filter(modulo=modulo)
                mLanzados = CumplimientoPasos.objects.filter(paso__nombre__iexact='lanzamiento').values('miembro')

                if 'aceptarAsistencia' in request.POST:
                    estudiantes = Matricula.objects.filter(Q(curso=curso), Q(moduloActual=modulo) | Q(moduloActual=None)).exclude(estudiante__id__in=mLanzados).order_by('estudiante__nombre')
                    seleccionados = request.POST.getlist('seleccionados')
                    for est in estudiantes:
                        if est.moduloActual is None:
                            est.moduloActual = modulo
                            est.save()

                        if str(est.id) in seleccionados:
                            try:
                                a = AsistenciaSesiones.objects.get(matricula=est, sesion=sesion)
                                a.asistencia = True
                            except:
                                a = AsistenciaSesiones.objects.create(matricula=est, sesion=sesion, asistencia = True, fecha=datetime.datetime.now())
                            a.save()
                            ok = True
                        else:
                            try:
                                a = AsistenciaSesiones.objects.get(matricula=est, sesion=sesion)
                                a.asistencia = False
                                a.save()
                                ok = True
                            except:
                                pass

                estudiantes = Matricula.objects.filter(Q(curso=curso), Q(moduloActual=modulo) | Q(moduloActual=None)).exclude(estudiante__id__in=mLanzados).order_by('estudiante__nombre')
                for est in estudiantes:
                    try:
                        a = AsistenciaSesiones.objects.get(sesion=sesion, matricula=est)
                        est.asistencia = a.asistencia
                    except:
                        est.asistencia = False
            except:
                raise Http404

        if not estudiantes:
            nadie = True
    miembro = Miembro.objects.get(usuario=request.user)
    cursos = Curso.objects.filter(profesor=miembro, estado='A')
    return render_to_response("Academia/asistencia.html", locals(), context_instance=RequestContext(request))


@user_passes_test(maestroTest, login_url="/dont_have_permissions/")
def maestroRegistrarEntregaTareas(request):
    """Permite a un maestro registrar si un estudiante entrego la tarea de una sesion. Se muestran solo
    los estudiantes que han dado dicha sesion."""

    if request.method == 'POST':
        if 'combo' in request.POST:
            if request.POST['combo'] == 'idCurso':
                curso = Curso.objects.get(id=request.POST['id'])
                modulos = curso.modulos.all()
                data = serializers.serialize('json', modulos)
            else:
                modulo = Modulo.objects.get(id=request.POST['id'])
                sesiones = Sesion.objects.filter(modulo=modulo)
                data = serializers.serialize('json', sesiones)
            return HttpResponse(data, content_type="application/javascript")

        if 'verEstudiantes' in request.POST or 'aceptarTarea' in request.POST:
            try:
                c = request.POST.getlist('menuCursos')[0]
                m = request.POST.getlist('menuModulos')[0]
                s = request.POST.getlist('menuSesiones')[0]

                curso = Curso.objects.get(id=c)
                modulo = Modulo.objects.get(id=m)
                sesion = Sesion.objects.get(id=s)
                modulos = curso.modulos.all()
                sesiones = Sesion.objects.filter(modulo=modulo)
                mLanzados = CumplimientoPasos.objects.filter(paso__nombre__iexact='lanzamiento').values('miembro')

                if 'aceptarTarea' in request.POST:
                    estudiantes = AsistenciaSesiones.objects.filter(asistencia=True, matricula__curso=curso, matricula__moduloActual=modulo, sesion=sesion).exclude(matricula__estudiante__id__in=mLanzados).order_by('matricula__estudiante__nombre')
                    seleccionados = request.POST.getlist('seleccionados')
                    for est in estudiantes:
                        if str(est.id) in seleccionados:
                            est.tarea = True
                        else:
                            est.tarea = False
                        est.save()
                        ok = True

                estudiantes = AsistenciaSesiones.objects.filter(asistencia=True, matricula__curso=curso, matricula__moduloActual=modulo, sesion=sesion).exclude(matricula__estudiante__id__in=mLanzados).order_by('matricula__estudiante__nombre')
                if len(estudiantes) == 0:
                    nadie = True
            except:
                raise Http404

    miembro = Miembro.objects.get(usuario=request.user)
    cursos = Curso.objects.filter(profesor=miembro, estado='A')
    return render_to_response("Academia/tareas.html", locals(), context_instance=RequestContext(request))


@user_passes_test(maestroTest, login_url="/dont_have_permissions/")
def evaluarModulo(request):
    """Permite a un profesor registrar la calificacion del examen final del modulo actual en el que se
    encuentra el estudiante, siempre y cuando este halla asistido a todas las sesiones de dicho modulo."""

    if request.method == 'POST':
        if request.session.get('actual') != None:
            actual = request.session['actual']  # estudiante actual
            try:
                estudiante_actual = Matricula.objects.get(id=actual)
                reporte = Reporte.objects.get(matricula=estudiante_actual, modulo=estudiante_actual.moduloActual)
                form = FormularioEvaluarModulo(data=request.POST, instance=reporte)
                sw = True
            except:
                form = FormularioEvaluarModulo(data=request.POST)
                sw = False

            if form.is_valid():
                nuevoReporte = form.save(commit=sw)
                if not sw:
                    nuevoReporte.matricula = estudiante_actual
                    nuevoReporte.modulo = estudiante_actual.moduloActual
                    nuevoReporte.save()
                total = estudiante_actual.curso.modulos.all().aggregate(Sum('porcentaje'))
                estudiante_actual.notaDefinitiva = estudiante_actual.notaDefinitiva + (nuevoReporte.nota*nuevoReporte.modulo.porcentaje/total['porcentaje__sum'])
                estudiante_actual.save()
                ok = True

    if 'seleccionados' in request.session:
            faltantes = request.session['seleccionados']
            if len(faltantes) > 0:
                estudiante = Matricula.objects.get(id=request.session['seleccionados'].pop())
                request.session['actual'] = int(estudiante.id)
                request.session['seleccionados'] = request.session['seleccionados']
                puedeVer = estudiante.asistioTodasSesiones()
                try:
                    reporte = Reporte.objects.get(matricula=estudiante, modulo=estudiante.moduloActual)
                    form = FormularioEvaluarModulo(instance=reporte)
                except:
                    form = FormularioEvaluarModulo()
            else:
                return HttpResponseRedirect("/academia/estudiantes/" + request.session['curso'] + "/")

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('Academia/evaluar_modulo.html', locals(), context_instance=RequestContext(request))


@user_passes_test(maestroTest, login_url="/dont_have_permissions/")
def promoverModulo(request):
    """Permite a un maestro promover a un estudiante de modulo, siempre y cuando este haya realizado el examen final
       de el modulo actual en el que se encuentra."""

    if request.method == 'POST':
        if request.session.get('actual') != None:
            actual = request.session['actual']
            est = Matricula.objects.get(id=actual)
            form = FormularioPromoverModulo(data=request.POST, instance=est)
            if form.is_valid():
                estudiantePromovido = form.save()
                ok = True

    if 'seleccionados' in request.session:
            faltantes = request.session['seleccionados']
            if len(faltantes) > 0:
                estudiante = Matricula.objects.get(id=request.session['seleccionados'].pop())
                request.session['actual'] = int(estudiante.id)
                request.session['seleccionados'] = request.session['seleccionados']
                puedeVer = estudiante.moduloReportado()
                form = FormularioPromoverModulo(est=estudiante, instance=estudiante)
            else:
                request.session['to-middleware'] = True
                return HttpResponseRedirect("/academia/estudiantes/" + request.session['curso'] + "/")

    miembro = Miembro.objects.get(usuario=request.user)
    return render_to_response('Academia/promover_estudiante.html', locals(), context_instance=RequestContext(request))

#  --------------------------------------------ADMINISTRADOR--------------------------------------------


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearCurso(request):
    """Permite a un administrador crear cursos en la academia."""

    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    url = '/academia/listar_cursos/'

    if request.method == "POST":
        form = FormularioCrearCurso(data=request.POST)
        if form.is_valid():
            nuevoCurso = form.save()
            form.full_clean()
            ok = True
    else:
        form = FormularioCrearCurso()

    return render_to_response('Academia/crear_curso.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def matricularEstudiante(request, id):
    """ Permite a un administrador matricular a un miembro de la iglesia en un curso de la academia siempre y cuando este
        haya realizado encuentro."""

    miembro = Miembro.objects.get(usuario=request.user)
    form = FormularioMatricula()

    if request.method == 'POST':
        form = FormularioMatricula(data=request.POST)
        if form.is_valid():
            nuevaMatricula = form.save(commit=False)
            nuevaMatricula.curso = Curso.objects.get(id=int(id))
            nuevaMatricula.save()
            ok = True

    return render_to_response('Academia/matricula.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def listarModulos(request):
    """Permite a un administrador listar los modulos de la academia."""

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            modulosEliminar = request.POST.getlist('seleccionados')
            okElim = eliminar(request, Modulo, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')

    modulos = Modulo.objects.all().order_by('id')
    return render_to_response('Academia/listar_modulos.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearModulo(request):
    """Permite a un administrador crear modulos en la academia."""

    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = FormularioCrearModulo(data=request.POST)
        if form.is_valid():
            nuevoModulo = form.save()
            ok = True

    form = FormularioCrearModulo()
    return render_to_response('Academia/crear_modulo.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def editarModulo(request, pk):
    """Permite a un administrador editar los modulos existentes en la academia."""

    accion = 'Editar'
    try:
        modulo = Modulo.objects.get(pk=pk)
    except Modulo.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = FormularioCrearModulo(request.POST or None, instance=modulo)

        if form.is_valid():
            form.save()
            ok = True
        else:
            print("Formulario Incorrecto")

    else:
        form = FormularioCrearModulo(instance=modulo)
        return render_to_response("Academia/crear_modulo.html", locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect("/academia/listar_modulos")


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def listarSesiones(request, id):
    """Permite a un administrador listar las sesiones de un modulo."""

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            okElim = eliminar(request, Sesion, request.POST.getlist('seleccionados'))
            if okElim == 1:
                return HttpResponseRedirect('')

    miembro = Miembro.objects.get(usuario=request.user)
    modulo = Modulo.objects.get(id=int(id))
    sesiones = Sesion.objects.filter(modulo=modulo).order_by('id')
    return render_to_response('Academia/listar_sesiones.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def crearSesion(request, id):
    """Permite a un administrador crear una sesion en un modulo."""

    accion = 'Crear'
    miembro = Miembro.objects.get(usuario=request.user)
    modulo = Modulo.objects.get(id=int(id))

    if request.method == 'POST':
        form = FormularioCrearSesion(data=request.POST)
        if form.is_valid():
            sesion = form.save(commit=False)
            sesion.modulo = modulo
            sesion.save()
            ok = True

    form = FormularioCrearSesion()
    return render_to_response('Academia/crear_sesion.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def editarSesion(request, id, pk):
    """Permite a un administrador editar una sesion de un modulo de la academia."""
    # miembro = Miembro.objects.get(usuario = request.user)

    accion = 'Editar'
    modulo = Modulo.objects.get(id=int(id))

    try:
        sesion = Sesion.objects.get(pk=pk)
    except Sesion.DoesNotExist:
        raise Http404

    if request.method == 'POST':

        form = FormularioCrearSesion(request.POST or None, instance=sesion)
        if form.is_valid():
            sesionEditado = form.save()
            ok = True
        else:
            return render_to_response("Academia/crear_sesion.html", locals(), context_instance=RequestContext(request))

    # if 'seleccionados' in request.session:
    #     faltantes = request.session['seleccionados']
    #     if len(faltantes) > 0:
    #         sesionEditar = Sesion.objects.get(id = request.session['seleccionados'].pop())
    #         request.session['actual'] = sesionEditar
    #         request.session['seleccionados'] = request.session['seleccionados']
    #         form = FormularioCrearSesion(instance = sesionEditar)

    else:
        form = FormularioCrearSesion(instance=sesion)
        return render_to_response("Academia/crear_sesion.html", locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect("/academia/sesiones/" + id + "/")


@user_passes_test(receptorTest, login_url="/dont_have_permissions/")
def recibirPago(request, id):
    miembro = Miembro.objects.get(usuario=request.user)
    try:
        miembroRecibir = Matricula.objects.get(estudiante__id=int(id))
    except:
        raise Http404
    if request.method == 'POST':
        form = FormularioRecibirPago(data=request.POST, instance=miembroRecibir)
        if form.is_valid():
            matriculaPago = form.save(commit=False)
            try:
                matriculaExistente = Matricula.objects.get(estudiante=matriculaPago.estudiante)
                matriculaExistente.pago = matriculaPago.pago
                matriculaExistente.save()
            except:
                raise Http404
            ok = True
        else:
            ok = False
    else:
        form = FormularioRecibirPago(instance=miembroRecibir)
    return render_to_response('Academia/recibir_pago.html', locals(), context_instance=RequestContext(request))


@user_passes_test(adminTest, login_url="/dont_have_permissions/")
def listarPagosAcademia(request):
    miembro = Miembro.objects.get(usuario=request.user)
    grupos = request.user.groups.all()
    for g in grupos:
        if 'Receptor' in g.name:
            receptor = True
    matriculas = Matricula.objects.all()
    return render_to_response('Academia/listar_pago.html', locals(), context_instance=RequestContext(request))
