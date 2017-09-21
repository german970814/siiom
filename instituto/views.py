from django.forms import inlineformset_factory
from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Curso, Matricula, Modulo, Sesion
)
from .forms import (
    FormularioMateria, FormularioModulo, FormularioSesion
)

__author__ = 'German Alzate'


def crear_materia(request):
    """
    Vista de creación de una materia, también sirve para crear modulos y sesiones.
    """

    data = {}

    ModuloFormSet = inlineformset_factory(
        Materia, Modulo, fk_name='materia',
        form=FormularioModulo, min_num=1, extra=1,
        validate_min=True, can_delete=False
    )

    if request.method == 'POST':
        formulario_materia = FormularioMateria(request.POST)
        if formulario_materia.is_valid():
            materia = formulario_materia.save(commit=False)
            formulario_modulo 
            materia.save()
    else:
        formulario_materia = FormularioMateria()

    data['formulario_materia'] = formulario_materia

    return render(request, 'istituto/crear_materia.html', data)

# def eliminar(request, modelo, lista):
#     ok = 0  # No hay nada en la lista
#     if lista:
#         ok = 1  # Los borro todos
#         for e in lista:
#             try:
#                 modelo.objects.get(id=e).delete()
#             except ValueError as e:
#                 print(e)
#                 pass
#             except:
#                 ok = 2  # Hubo un Error
#     if ok == 1:
#         messages.success(request, "Se ha eliminado correctamente")
#     return ok

# #  -------------------------AMBOS----------------------------------


# # @user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
# def verCursos(request, admin):
#     """Permite a un maestro o a un administrador listar cursos."""
#     miembro = Miembro.objects.get(usuario=request.user)
#     # if miembro.usuario.has_perm("miembros.es_administrador"):
#     #     admin = True
#     # else:
#     #     admin = False

#     if request.method == 'POST':
#         request.session['seleccionados'] = request.POST.getlist('seleccionados')
#         if admin:
#             return HttpResponseRedirect('/academia/admin_editar_curso/')
#         else:
#             return HttpResponseRedirect("/academia/editar_curso/")

#     miembro = Miembro.objects.get(usuario=request.user)
#     if admin:
#         cursos = Curso.objects.all().order_by('estado', 'profesor__nombre')
#         request.session['admin'] = True
#     else:
#         cursos = Curso.objects.filter(profesor=miembro, estado='A')
#         request.session['admin'] = False
#     return render_to_response("academia/listar_cursos.html", locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
# def verDetalleCurso(request, curso):
#     """Permite a un maestro o administrador ver los modulos y sesiones que se dan en un curso."""

#     miembro = Miembro.objects.get(usuario=request.user)
#     iid = int(curso)
#     curso = Curso.objects.get(id=iid)
#     modulos = curso.modulos.all()
#     for modulo in modulos:
#         modulo.sesiones = Sesion.objects.filter(modulo=modulo)
#     return render_to_response("academia/curso_detalle.html", locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
# def editarCurso(request, admin, url, pk, template_name="academia/crear_curso.html"):
#     """Permite a un maestro o administrador editar un cursos."""
#     accion = 'Editar'
#     curso = get_object_or_404(Curso, pk=pk)

#     if request.method == 'POST':
#         if admin:
#             form = FormularioCrearCurso(request.POST or None, instance=curso)
#         else:
#             form = FormularioEditarCurso(request.POST or None, instance=curso)

#         if form.is_valid():
#             form.save()
#             if admin:
#                 return HttpResponseRedirect("/academia/listar_cursos")
#             else:
#                 return HttpResponseRedirect("/academia/mis-cursos/")
#     else:
#         if admin:
#             form = FormularioCrearCurso(instance=curso)
#         else:
#             form = FormularioEditarCurso(instance=curso)

#     return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
# def listarEstudiantes(request, curso):
#     """Permite listar los modulos dados en un curso y los estudiantes que asisten a dicho curso."""

#     if request.method == 'POST':
#         if 'Eliminar' in request.POST:
#             eliminar(request, Matricula, request.POST.getlist('seleccionados'))
#         else:
#             seleccionados = list()
#             for x in request.POST.getlist('seleccionados'):
#                 if isinstance(x, int):
#                     if x not in seleccionados:
#                         seleccionados.append(x)
#                 else:
#                     try:
#                         if x not in seleccionados:
#                             seleccionados.append(int(x))
#                     except ValueError:
#                         pass
#             sel = []
#             [sel.append(y) for y in seleccionados if y not in sel]
#             request.session['seleccionados'] = sel  # request.POST.getlist('seleccionados')
#             request.session['curso'] = request.POST['curso']
#             if request.POST['accion'] == 'M':
#                 return HttpResponseRedirect("/academia/evaluar_modulo/")
#             if request.POST['accion'] == 'P':
#                 return HttpResponseRedirect("/academia/promover_estudiante/")

#     # admin = request.session['admin']
#     miembro = Miembro.objects.get(usuario=request.user)
#     id = int(curso)
#     curso = Curso.objects.get(id=id)
#     # mLanzados = CumplimientoPasos.objects.filter(paso__nombre__iexact='lanzamiento').values('miembro')
#     # estudiantes = Matricula.objects.filter(curso=curso).exclude(estudiante__id__in=mLanzados)
#     estudiantes = Matricula.objects.filter(curso=curso)
#     for est in estudiantes:
#         totalSesiones = Sesion.objects.filter(modulo=est.modulo_actual).count()
#         est.sesionesDadas = AsistenciaSesiones.objects.filter(matricula=est, sesion__modulo=est.modulo_actual).count()
#         est.sesionesFaltantes = totalSesiones - est.sesionesDadas
#     return render_to_response("academia/listar_estudiantes.html", locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminMaestroTest, login_url="/dont_have_permissions/")
# def verDetalleEstudiante(request, est):
#     """Permite ver la informacion del estudiante. Las sesiones dadas, su nota definitiva, etc."""

#     miembro = Miembro.objects.get(usuario=request.user)
#     id = int(est)
#     try:
#         est = Matricula.objects.get(id=id)
#     except Matricula.DoesNotExist:
#         raise Http404
#     est.modulosDados = list(est.modulos.all())
#     if est.modulo_actual not in est.modulosDados and est.modulo_actual is not None:
#         est.modulosDados.append(est.modulo_actual)
#     for modulo in est.modulosDados:
#         try:
#             modulo.reporte = Reporte.objects.get(matricula=est, modulo=modulo)
#         except:
#             pass
#         modulo.sesiones = Sesion.objects.filter(modulo=modulo)
#         for sesion in modulo.sesiones:
#             try:
#                 sesion.asistencia = AsistenciaSesiones.objects.get(matricula=est, sesion=sesion)
#             except:
#                 pass
#     return render_to_response("academia/estudiante_detalle.html", locals(), context_instance=RequestContext(request))


# #  ----------------------------------MAESTRO--------------------------------------
# # @user_passes_test(maestroTest, login_url="/dont_have_permissions/")
# def maestroAsistencia(request):
#     """ Permite a un maestro llenar la asistencia de una sesion. Se muestran los estudiantes que esten en dicho modulo
#         o que el modulo_actual sea None."""

#     if request.method == 'POST':
#         if 'combo' in request.POST:
#             if request.POST['combo'] == 'idCurso':
#                 curso = Curso.objects.get(id=request.POST['id'])
#                 modulos = curso.modulos.all()
#                 data = serializers.serialize('json', modulos)
#             else:
#                 modulo = Modulo.objects.get(id=request.POST['id'])
#                 sesiones = Sesion.objects.filter(modulo=modulo)
#                 data = serializers.serialize('json', sesiones)
#             return HttpResponse(data, content_type="application/javascript")

#         if 'verEstudiantes' in request.POST or 'aceptarAsistencia' in request.POST:
#             # try:
#             c = request.POST.getlist('menuCursos')[0]
#             m = request.POST.getlist('menuModulos')[0]
#             s = request.POST.getlist('menuSesiones')[0]

#             curso = Curso.objects.get(id=c)
#             modulo = Modulo.objects.get(id=m)
#             sesion = Sesion.objects.get(id=s)
#             modulos = curso.modulos.all()
#             sesiones = Sesion.objects.filter(modulo=modulo)
#             # mLanzados = CumplimientoPasos.objects.filter(paso__nombre__iexact='lanzamiento').values('miembro')

#             if 'aceptarAsistencia' in request.POST:
#                 # estudiantes = Matricula.objects.filter(
#                 #     Q(curso=curso),
#                 #     Q(modulo_actual=modulo) | Q(modulo_actual=None)
#                 # ).exclude(estudiante__id__in=mLanzados).order_by('estudiante__nombre')
#                 estudiantes = Matricula.objects.filter(
#                     Q(curso=curso),
#                     Q(modulo_actual=modulo) | Q(modulo_actual=None)
#                 ).order_by('estudiante__nombre')
#                 seleccionados = request.POST.getlist('seleccionados')
#                 for est in estudiantes:
#                     if est.modulo_actual is None:
#                         est.modulo_actual = modulo
#                         est.save()

#                     if str(est.id) in seleccionados:
#                         try:
#                             a = AsistenciaSesiones.objects.get(matricula=est, sesion=sesion)
#                             a.asistencia = True
#                         except:
#                             a = AsistenciaSesiones.objects.create(
#                                 matricula=est, sesion=sesion,
#                                 asistencia=True, fecha=datetime.datetime.now())
#                         a.save()
#                         ok = True
#                     else:
#                         try:
#                             a = AsistenciaSesiones.objects.get(matricula=est, sesion=sesion)
#                             a.asistencia = False
#                             a.save()
#                             ok = True
#                         except:
#                             pass

#             # estudiantes = Matricula.objects.filter(
#             #     Q(curso=curso), Q(modulo_actual=modulo) | Q(modulo_actual=None)
#             # ).exclude(estudiante__id__in=mLanzados).order_by('estudiante__nombre')
#             estudiantes = Matricula.objects.filter(
#                 Q(curso=curso), Q(modulo_actual=modulo) | Q(modulo_actual=None)
#             ).order_by('estudiante__nombre')
#             for est in estudiantes:
#                 try:
#                     a = AsistenciaSesiones.objects.get(sesion=sesion, matricula=est)
#                     est.asistencia = a.asistencia
#                 except:
#                     est.asistencia = False
#             # except:
#             #     raise Http404

#         if not estudiantes:
#             nadie = True
#     miembro = Miembro.objects.get(usuario=request.user)
#     cursos = Curso.objects.filter(profesor=miembro, estado='A')
#     return render_to_response("academia/asistencia.html", locals(), context_instance=RequestContext(request))


# # @user_passes_test(maestroTest, login_url="/dont_have_permissions/")
# def maestroRegistrarEntregaTareas(request):
#     """Permite a un maestro registrar si un estudiante entrego la tarea de una sesion. Se muestran solo
#     los estudiantes que han dado dicha sesion."""

#     if request.method == 'POST':
#         if 'combo' in request.POST:
#             if request.POST['combo'] == 'idCurso':
#                 curso = Curso.objects.get(id=request.POST['id'])
#                 modulos = curso.modulos.all()
#                 data = serializers.serialize('json', modulos)
#             else:
#                 modulo = Modulo.objects.get(id=request.POST['id'])
#                 sesiones = Sesion.objects.filter(modulo=modulo)
#                 data = serializers.serialize('json', sesiones)
#             return HttpResponse(data, content_type="application/javascript")

#         if 'verEstudiantes' in request.POST or 'aceptarTarea' in request.POST:
#             # try:
#             c = request.POST.getlist('menuCursos')[0]
#             m = request.POST.getlist('menuModulos')[0]
#             s = request.POST.getlist('menuSesiones')[0]

#             curso = Curso.objects.get(id=c)
#             modulo = Modulo.objects.get(id=m)
#             sesion = Sesion.objects.get(id=s)
#             modulos = curso.modulos.all()
#             sesiones = Sesion.objects.filter(modulo=modulo)
#             # mLanzados = CumplimientoPasos.objects.filter(paso__nombre__iexact='lanzamiento').values('miembro')

#             if 'aceptarTarea' in request.POST:
#                 # estudiantes = AsistenciaSesiones.objects.filter(
#                 #     asistencia=True, matricula__curso=curso,
#                 #     matricula__modulo_actual=modulo, sesion=sesion
#                 # ).exclude(matricula__estudiante__id__in=mLanzados).order_by('matricula__estudiante__nombre')
#                 estudiantes = AsistenciaSesiones.objects.filter(
#                     asistencia=True, matricula__curso=curso,
#                     matricula__modulo_actual=modulo, sesion=sesion
#                 ).order_by('matricula__estudiante__nombre')
#                 seleccionados = request.POST.getlist('seleccionados')
#                 for est in estudiantes:
#                     if str(est.id) in seleccionados:
#                         est.tarea = True
#                     else:
#                         est.tarea = False
#                     est.save()
#                     ok = True

#             # estudiantes = AsistenciaSesiones.objects.filter(
#             #     asistencia=True, matricula__curso=curso, matricula__modulo_actual=modulo,
#             #     sesion=sesion
#             # ).exclude(matricula__estudiante__id__in=mLanzados).order_by('matricula__estudiante__nombre')
#             estudiantes = AsistenciaSesiones.objects.filter(
#                 asistencia=True, matricula__curso=curso, matricula__modulo_actual=modulo,
#                 sesion=sesion
#             ).order_by('matricula__estudiante__nombre')
#             if len(estudiantes) == 0:
#                 nadie = True
#             # except:
#             #     raise Http404

#     miembro = Miembro.objects.get(usuario=request.user)
#     cursos = Curso.objects.filter(profesor=miembro, estado='A')
#     return render_to_response("academia/tareas.html", locals(), context_instance=RequestContext(request))


# # @user_passes_test(maestroTest, login_url="/dont_have_permissions/")
# def evaluarModulo(request):
#     """Permite a un profesor registrar la calificacion del examen final del modulo actual en el que se
#     encuentra el estudiante, siempre y cuando este halla asistido a todas las sesiones de dicho modulo."""

#     if request.method == 'POST':
#         if request.session.get('actual') is not None:
#             actual = request.session['actual']  # estudiante actual
#             try:
#                 estudiante_actual = Matricula.objects.get(id=actual)
#                 reporte = Reporte.objects.get(matricula=estudiante_actual, modulo=estudiante_actual.modulo_actual)
#                 form = FormularioEvaluarModulo(data=request.POST, instance=reporte)
#                 sw = True
#             except:
#                 form = FormularioEvaluarModulo(data=request.POST)
#                 sw = False

#             if form.is_valid():
#                 nuevoReporte = form.save(commit=sw)
#                 if not sw:
#                     nuevoReporte.matricula = estudiante_actual
#                     nuevoReporte.modulo = estudiante_actual.modulo_actual
#                     nuevoReporte.save()
#                 total = estudiante_actual.curso.modulos.all().aggregate(Sum('porcentaje'))
#                 estudiante_actual.nota_definitiva = estudiante_actual.nota_definitiva + \
#                     (nuevoReporte.nota * nuevoReporte.modulo.porcentaje / total['porcentaje__sum'])
#                 estudiante_actual.save()
#                 ok = True

#     if 'seleccionados' in request.session:
#             faltantes = request.session['seleccionados']
#             if len(faltantes) > 0:
#                 estudiante = Matricula.objects.get(id=request.session['seleccionados'].pop())
#                 request.session['actual'] = int(estudiante.id)
#                 request.session['seleccionados'] = request.session['seleccionados']
#                 puedeVer = estudiante.asistio_todas_las_sesiones()
#                 try:
#                     reporte = Reporte.objects.get(matricula=estudiante, modulo=estudiante.modulo_actual)
#                     form = FormularioEvaluarModulo(instance=reporte)
#                 except:
#                     form = FormularioEvaluarModulo()
#             else:
#                 return HttpResponseRedirect("/academia/estudiantes/" + request.session['curso'] + "/")

#     miembro = Miembro.objects.get(usuario=request.user)
#     return render_to_response('academia/evaluar_modulo.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(maestroTest, login_url="/dont_have_permissions/")
# def promoverModulo(request):
#     """Permite a un maestro promover a un estudiante de modulo, siempre y cuando este haya realizado el examen final
#        de el modulo actual en el que se encuentra."""

#     if request.method == 'POST':
#         if request.session.get('actual') is not None:
#             actual = request.session['actual']
#             est = Matricula.objects.get(id=actual)
#             form = FormularioPromoverModulo(data=request.POST, instance=est)
#             if form.is_valid():
#                 estudiantePromovido = form.save()
#                 ok = True

#     if 'seleccionados' in request.session:
#             faltantes = request.session['seleccionados']
#             if len(faltantes) > 0:
#                 estudiante = Matricula.objects.get(id=request.session['seleccionados'].pop())
#                 request.session['actual'] = int(estudiante.id)
#                 request.session['seleccionados'] = request.session['seleccionados']
#                 puedeVer = estudiante.modulo_reportado()
#                 form = FormularioPromoverModulo(est=estudiante, instance=estudiante)
#             else:
#                 request.session['to-middleware'] = True
#                 return HttpResponseRedirect("/academia/estudiantes/" + request.session['curso'] + "/")

#     miembro = Miembro.objects.get(usuario=request.user)
#     return render_to_response('academia/promover_estudiante.html', locals(), context_instance=RequestContext(request))

# #  --------------------------------------------ADMINISTRADOR--------------------------------------------


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def crearCurso(request):
#     """Permite a un administrador crear cursos en la academia."""

#     accion = 'Crear'
#     miembro = Miembro.objects.get(usuario=request.user)
#     url = '/academia/listar_cursos/'

#     if request.method == "POST":
#         form = FormularioCrearCurso(data=request.POST)
#         if form.is_valid():
#             nuevoCurso = form.save()
#             form.full_clean()
#             ok = True
#     else:
#         form = FormularioCrearCurso()

#     return render_to_response('academia/crear_curso.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def matricularEstudiante(request, id):
#     """ Permite a un administrador matricular a un miembro de la iglesia en un curso de la academia siempre y cuando este
#         haya realizado encuentro."""

#     miembro = Miembro.objects.get(usuario=request.user)
#     form = FormularioMatricula()

#     if request.method == 'POST':
#         form = FormularioMatricula(data=request.POST)
#         if form.is_valid():
#             nuevaMatricula = form.save(commit=False)
#             nuevaMatricula.curso = Curso.objects.get(id=int(id))
#             nuevaMatricula.save()
#             ok = True

#     return render_to_response('academia/matricula.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def listarModulos(request):
#     """Permite a un administrador listar los modulos de la academia."""

#     if request.method == 'POST':
#         if 'eliminar' in request.POST:
#             modulosEliminar = request.POST.getlist('seleccionados')
#             okElim = eliminar(request, Modulo, request.POST.getlist('seleccionados'))
#             if okElim == 1:
#                 return HttpResponseRedirect('')

#     modulos = Modulo.objects.all().order_by('id')
#     return render_to_response('academia/listar_modulos.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def crearModulo(request):
#     """Permite a un administrador crear modulos en la academia."""

#     accion = 'Crear'
#     miembro = Miembro.objects.get(usuario=request.user)

#     if request.method == 'POST':
#         form = FormularioCrearModulo(data=request.POST)
#         if form.is_valid():
#             nuevoModulo = form.save()
#             ok = True

#     form = FormularioCrearModulo()
#     return render_to_response('academia/crear_modulo.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def editarModulo(request, pk):
#     """Permite a un administrador editar los modulos existentes en la academia."""

#     accion = 'Editar'
#     try:
#         modulo = Modulo.objects.get(pk=pk)
#     except Modulo.DoesNotExist:
#         raise Http404

#     if request.method == 'POST':
#         form = FormularioCrearModulo(request.POST or None, instance=modulo)

#         if form.is_valid():
#             form.save()
#             ok = True
#         else:
#             print("Formulario Incorrecto")

#     else:
#         form = FormularioCrearModulo(instance=modulo)
#         return render_to_response("academia/crear_modulo.html", locals(), context_instance=RequestContext(request))

#     return HttpResponseRedirect("/academia/listar_modulos")


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def listarSesiones(request, id):
#     """Permite a un administrador listar las sesiones de un modulo."""

#     if request.method == 'POST':
#         if 'eliminar' in request.POST:
#             okElim = eliminar(request, Sesion, request.POST.getlist('seleccionados'))
#             if okElim == 1:
#                 return HttpResponseRedirect('')

#     miembro = Miembro.objects.get(usuario=request.user)
#     modulo = Modulo.objects.get(id=int(id))
#     sesiones = Sesion.objects.filter(modulo=modulo).order_by('id')
#     return render_to_response('academia/listar_sesiones.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def crearSesion(request, id):
#     """Permite a un administrador crear una sesion en un modulo."""

#     accion = 'Crear'
#     miembro = Miembro.objects.get(usuario=request.user)
#     modulo = Modulo.objects.get(id=int(id))

#     if request.method == 'POST':
#         form = FormularioCrearSesion(data=request.POST)
#         if form.is_valid():
#             sesion = form.save(commit=False)
#             sesion.modulo = modulo
#             sesion.save()
#             ok = True

#     form = FormularioCrearSesion()
#     return render_to_response('academia/crear_sesion.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def editarSesion(request, id, pk):
#     """Permite a un administrador editar una sesion de un modulo de la academia."""
#     # miembro = Miembro.objects.get(usuario = request.user)

#     accion = 'Editar'
#     modulo = Modulo.objects.get(id=int(id))

#     try:
#         sesion = Sesion.objects.get(pk=pk)
#     except Sesion.DoesNotExist:
#         raise Http404

#     if request.method == 'POST':

#         form = FormularioCrearSesion(request.POST or None, instance=sesion)
#         if form.is_valid():
#             sesionEditado = form.save()
#             ok = True
#         else:
#             return render_to_response("academia/crear_sesion.html", locals(), context_instance=RequestContext(request))

#     # if 'seleccionados' in request.session:
#     #     faltantes = request.session['seleccionados']
#     #     if len(faltantes) > 0:
#     #         sesionEditar = Sesion.objects.get(id = request.session['seleccionados'].pop())
#     #         request.session['actual'] = sesionEditar
#     #         request.session['seleccionados'] = request.session['seleccionados']
#     #         form = FormularioCrearSesion(instance = sesionEditar)

#     else:
#         form = FormularioCrearSesion(instance=sesion)
#         return render_to_response("academia/crear_sesion.html", locals(), context_instance=RequestContext(request))

#     return HttpResponseRedirect("/academia/sesiones/" + id + "/")


# # @user_passes_test(receptorTest, login_url="/dont_have_permissions/")
# def recibirPago(request, id):
#     miembro = Miembro.objects.get(usuario=request.user)
#     try:
#         miembroRecibir = Matricula.objects.get(estudiante__id=int(id))
#     except:
#         raise Http404
#     if request.method == 'POST':
#         form = FormularioRecibirPago(data=request.POST, instance=miembroRecibir)
#         if form.is_valid():
#             matriculaPago = form.save(commit=False)
#             try:
#                 matriculaExistente = Matricula.objects.get(estudiante=matriculaPago.estudiante)
#                 matriculaExistente.pago = matriculaPago.pago
#                 matriculaExistente.save()
#             except:
#                 raise Http404
#             ok = True
#         else:
#             ok = False
#     else:
#         form = FormularioRecibirPago(instance=miembroRecibir)
#     return render_to_response('academia/recibir_pago.html', locals(), context_instance=RequestContext(request))


# # @user_passes_test(adminTest, login_url="/dont_have_permissions/")
# def listarPagosAcademia(request):
#     miembro = Miembro.objects.get(usuario=request.user)
#     grupos = request.user.groups.all()
#     for g in grupos:
#         if 'Receptor' in g.name:
#             receptor = True
#     matriculas = Matricula.objects.all()
#     return render_to_response('academia/listar_pago.html', locals(), context_instance=RequestContext(request))


def lista_estudiantes_sesion(request):
    from django.shortcuts import render
    return render(request, 'academia/lista_estudiantes_sesion.html', {})
