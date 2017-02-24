# -*- coding: utf-8 -*-
'''
Created on Apr 4, 2011

@author: Migue
'''
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _lazy
from miembros.models import Miembro, Zona, Barrio, CumplimientoPasos,\
    Pasos, Escalafon, CambioEscalafon, TipoMiembro, CambioTipo, DetalleLlamada
from django.db.models import Q
from django import forms
from academia.models import Matricula
from grupos.models import Grupo
from PIL import Image
from io import BytesIO
from common.forms import CustomForm, CustomModelForm
from grupos.forms import ArchivarGrupoForm


class FormularioLiderAgregarMiembro(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, g='', c=None, *args, **kwargs):
        super(FormularioLiderAgregarMiembro, self).__init__(*args, **kwargs)  # populates the post
        if g != '':
            if g == 'M':
                g = 'F'
            else:
                g = 'M'

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['primerApellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundoApellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['celular'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['fechaNacimiento'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/0000'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['profesion'].widget.attrs.update({'class': 'form-control'})
        self.fields['barrio'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['genero'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['estadoCivil'].widget.attrs.update({'class': 'selectpicker'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control'})
        # if c:
        #     self.fields['conyugue'].queryset = Miembro.objects.filter(
        #         Q(estadoCivil='S')|Q(estadoCivil='V')| Q(estadoCivil='D')| Q(id=c.id), genero=g)
        # else:
        #     self.fields['conyugue'].queryset = Miembro.objects.filter(
        #         Q(estadoCivil='S')|Q(estadoCivil='V')| Q(estadoCivil='D'), genero=g)

    class Meta:
        model = Miembro
        fields = (
            'nombre', 'primerApellido', 'segundoApellido', 'telefono',
            'celular', 'direccion', 'fechaNacimiento', 'cedula', 'email',
            'profesion', 'barrio', 'genero', 'estadoCivil'  # , 'conyugue'
        )
        # exclude = ('usuario', 'grupo', 'lider', 'pasos', 'escalafon', 'fechaAsignacionGAR',
        #            'asignadoGAR', 'asisteGAR', ''
        #            'fechaLlamadaLider', 'detalleLlamadaLider', 'observacionLlamadaLider',
        #            'fechaPrimeraLlamada', 'detallePrimeraLlamada', 'observacionPrimeraLlamada',
        #            'fechaSegundaLlamada', 'detalleSegundaLlamada', 'observacionSegundaLlamada',
        #            'noInteresadoGAR', 'convertido', 'estado', 'conyugue', 'foto_perfil', 'iglesia')


class FormularioAdminAgregarMiembro(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, g='', *args, **kwargs):
        super(FormularioAdminAgregarMiembro, self).__init__(*args, **kwargs)  # populates the post
        if g != '':
            if g == 'M':
                g = 'F'
            else:
                g = 'M'
            queryset = Miembro.objects.filter(Q(estadoCivil='S') | Q(estadoCivil='V') | Q(estadoCivil='D'), genero=g)
            self.fields['conyugue'].queryset = queryset

            if self.instance.conyugue:
                conyugue = Miembro.objects.filter(id=self.instance.conyugue.id)
                self.fields['conyugue'].queryset = queryset | conyugue

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['primerApellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundoApellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['celular'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['fechaNacimiento'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/0000'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['profesion'].widget.attrs.update({'class': 'form-control'})
        self.fields['barrio'].widget.attrs.update({'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['estadoCivil'].widget.attrs.update({'class': 'selectpicker'})
        # self.fields['estado'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['conyugue'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

    class Meta:
        model = Miembro
        fields = (
            'nombre', 'primerApellido', 'segundoApellido', 'telefono',
            'celular', 'direccion', 'fechaNacimiento', 'cedula', 'email',
            'profesion', 'barrio', 'genero', 'estadoCivil', 'conyugue'
        )
        # exclude = ('usuario', 'grupo', 'lider', 'pasos', 'escalafon', 'fechaAsignacionGAR',
        #            'fechaLlamadaLider', 'detalleLlamadaLider', 'observacionLlamadaLider',
        #            'fechaPrimeraLlamada', 'detallePrimeraLlamada', 'observacionPrimeraLlamada',
        #            'fechaSegundaLlamada', 'detalleSegundaLlamada', 'observacionSegundaLlamada',
        #            'estado', 'iglesia')


class FormularioLlamadaLider(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioLlamadaLider, self).__init__(*args, **kwargs)

        self.fields['detalleLlamadaLider'].widget.attrs.update({'class': 'form-control'})
        self.fields['observacionLlamadaLider'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Miembro
        fields = ('detalleLlamadaLider', 'observacionLlamadaLider')


class FormularioPrimeraLlamadaAgente(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioPrimeraLlamadaAgente, self).__init__(*args, **kwargs)
        self.fields['detallePrimeraLlamada'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['observacionPrimeraLlamada'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Miembro
        fields = ('detallePrimeraLlamada',
                  'observacionPrimeraLlamada',
                  'noInteresadoGAR',
                  'asisteGAR',
                  'asignadoGAR',
                  'fechaAsignacionGAR',
                  'grupo')


class FormularioSegundaLlamadaAgente(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioSegundaLlamadaAgente, self).__init__(*args, **kwargs)
        self.fields['detalleSegundaLlamada'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['observacionSegundaLlamada'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Miembro
        fields = ('detalleSegundaLlamada', 'observacionSegundaLlamada', 'asisteGAR', 'noInteresadoGAR')


class FormularioCambiarContrasena(forms.Form):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    contrasenaAnterior = forms.CharField(
        widget=forms.PasswordInput(render_value=False), max_length=20, label='Contraseña anterior:')
    contrasenaNueva = forms.CharField(
        widget=forms.PasswordInput(render_value=False), max_length=20, label='Contraseña nueva:')
    contrasenaNuevaVerificacion = forms.CharField(
        widget=forms.PasswordInput(render_value=False), max_length=20, label='Verifique contraseña nueva:')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(FormularioCambiarContrasena, self).__init__(*args, **kwargs)

    def clean(self):
        cont_vieja = self.data['contrasenaAnterior']
        usuario = self.request.user

        if not usuario.check_password(cont_vieja):
            self.add_error('contrasenaAnterior', "Rectifica la Contraseña")
            raise forms.ValidationError("Contraseña Incorrecta")

        if self.data['contrasenaNueva'] != self.data['contrasenaNuevaVerificacion']:
            self.add_error('contrasenaNuevaVerificacion', "Tus contraseñas no coinciden")
            raise forms.ValidationError("Contraseñas no coinciden")

        return super(FormularioCambiarContrasena, self).clean()


class FormularioAsignarGrupo(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioAsignarGrupo, self).__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

    class Meta:
        model = Miembro
        fields = ('grupo', )


class FormularioCrearZona(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearZona, self).__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].required = True

    def clean(self):
        nam = self.cleaned_data.get('nombre')

        if not nam:
            self.add_error('nombre', "Este campo es requerido")
        return super(FormularioCrearZona, self).clean()

    class Meta:
        model = Zona
        fields = ('nombre', )


class FormularioCrearBarrio(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearBarrio, self).__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Barrio
        fields = ('nombre', )


class FormularioPasosMiembro(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    class Meta:
        model = CumplimientoPasos
        fields = ('paso',)


class FormularioCumplimientoPasosMiembro(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioCumplimientoPasosMiembro, self).__init__(*args, **kwargs)  # populates the post
        estudiantes = Matricula.objects.all().exclude(
            estudiante__pasos__nombre__iexact='lanzamiento').values('estudiante')
        self.fields['miembro'].queryset = Miembro.objects.filter(id__in=estudiantes)
        self.fields['miembro'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

    class Meta:
        model = CumplimientoPasos
        fields = ('miembro',)


class FormularioPasos(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioPasos, self).__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioridad'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Pasos
        fields = '__all__'


class FormularioCrearEscalafon(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearEscalafon, self).__init__(*args, **kwargs)

        self.fields['celulas'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción...'})
        self.fields['logro'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Logros...'})
        self.fields['rango'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Escalafon
        fields = '__all__'


class FormularioPromoverEscalafon(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioPromoverEscalafon, self).__init__(*args, **kwargs)
        self.fields['miembro'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['escalafon'].widget.attrs.update({'class': 'selectpicker'})

    class Meta:
        model = CambioEscalafon
        fields = ('miembro', 'escalafon')


class FormularioCrearTipoMiembro(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearTipoMiembro, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = TipoMiembro
        fields = ('nombre', )


class FormularioCambioTipoMiembro(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, idm='', *args, **kwargs):
        super(FormularioCambioTipoMiembro, self).__init__(*args, **kwargs)  # populates the post
        self.fields['nuevoTipo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.idm = idm
        if idm != '':
            m = Miembro.objects.get(id=idm)
            tipos = CambioTipo.objects.filter(miembro=m).values('nuevoTipo')
            self.fields['nuevoTipo'].queryset = TipoMiembro.objects.all().exclude(id__in=tipos)
#            try:
#                mLanzado = CumplimientoPasos.objects.get(miembro = m, paso__nombre__iexact = 'lanzamiento')
#            except:
#                mLanzado = None
#            if mLanzado is None:
#                self.fields['nuevoTipo'].queryset = self.fields['nuevoTipo'].queryset.exclude(nombre__iexact = 'lider')

    class Meta:
        model = CambioTipo
        fields = ('nuevoTipo', )


class FormularioAsignarUsuario(forms.Form):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    email = forms.EmailField(label='Verificar correo:')
    contrasena = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=20, label='Contraseña:')
    contrasenaVerificacion = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                             max_length=20, label='Verifique contraseña:')

    def __init__(self, *args, **kwargs):
        super(FormularioAsignarUsuario, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['contrasena'].widget.attrs.update({'class': 'form-control'})
        self.fields['contrasenaVerificacion'].widget.attrs.update({'class': 'form-control'})


class FormularioDetalleLlamada(ModelForm):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioDetalleLlamada, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = DetalleLlamada
        fields = '__all__'


class FormularioRecuperarContrasenia(forms.Form):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(FormularioRecuperarContrasenia, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ejemplo@iglesia.com'})


class FormularioFotoPerfil(forms.ModelForm):
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        return super(FormularioFotoPerfil, self).__init__(*args, **kwargs)

    def clean_foto_perfil(self):
        foto = self.cleaned_data['foto_perfil']

        if foto is None:
            foto = 'static/Imagenes/log.jpg'

        try:
            from django.core.files.images import get_image_dimensions

            w, h = get_image_dimensions(foto)

            max_width = max_height = 2000

            if w > max_width or h > max_height:
                self.add_error('foto_perfil', 'Tamaño maximo aceptado de %sx%s y has puesto una de \
                    %sx%s' % (max_width, max_height, w, h))

            # main, sub = foto.content_type.split('/')
            # if not(main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            #     self.add_error('foto_perfil', 'Error con el tipo de imagen')

            # if len(foto) > (20 * 1024):
            #     print("Error exceso de tamaño")

        except AttributeError as e:
            print(e)
            pass

        return foto

    def clean(self):
        return super(FormularioFotoPerfil, self).clean()

    def save(self, commit=True):
        image_field = self.cleaned_data.get('foto_perfil')
        image_file = BytesIO(image_field.read())
        image = Image.open(image_file)
        w, h = image.size

        # if w > 1000 or h > 1000:
        #     image = image.resize((1000, 1000), Image.ANTIALIAS)
        # if w < 400 or h < 400:
        #     image = image.resize((400, 400), Image.ANTIALIAS)

        image_file = BytesIO()
        image.save(image_file, 'png', quality=90)

        image_field.file = image_file

        return super(FormularioFotoPerfil, self).save(commit=commit)

    class Meta:
        model = Miembro
        fields = ('foto_perfil', )


class FormularioInformacionIglesiaMiembro(forms.ModelForm):
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioInformacionIglesiaMiembro, self).__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs.update({'class': 'selectpicker'})

    class Meta:
        model = Miembro
        fields = ('estado', 'convertido', 'asisteGAR', 'asignadoGAR')


class FormularioTipoMiembros(forms.ModelForm):
    error_css_class = 'has-error'

    tipos = forms.ModelMultipleChoiceField(queryset=TipoMiembro.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(FormularioTipoMiembros, self).__init__(*args, **kwargs)
        if self.instance:
            tipos = CambioTipo.objects.filter(miembro=self.instance)
            self.fields['tipos'].initial = [tipo.nuevoTipo.id for tipo in tipos]
            # self.fields['tipos'].required = False

    class Meta:
        model = CambioTipo
        exclude = ('miembro', 'autorizacion', 'nuevoTipo', 'anteriorTipo', 'fecha')


class NuevoMiembroForm(CustomModelForm):
    """
    Formulario para la creación de un miembro de una iglesia.
    """

    class Meta:
        model = Miembro
        fields = [
            'nombre', 'primerApellido', 'segundoApellido', 'genero', 'telefono', 'celular', 'fechaNacimiento',
            'cedula', 'direccion', 'barrio', 'email', 'profesion', 'estadoCivil'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['celular'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['profesion'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['estadoCivil'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['primerApellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundoApellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['fechaNacimiento'].widget.attrs.update({'class': 'form-control'})
        self.fields['barrio'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

    def save(self, iglesia):
        self.instance.iglesia = iglesia
        return super().save()


class TrasladarMiembroForm(CustomForm):
    """
    Formulario para el traslado de un miembro de un grupo a otro.
    """

    nuevo = forms.ModelChoiceField(
        queryset=Grupo.objects.prefetch_related('lideres').all(), label=_lazy('Trasladar a')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nuevo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

    def trasladar(self, miembro):
        miembro.trasladar(self.cleaned_data['nuevo'])


class DesvincularLiderGrupoForm(ArchivarGrupoForm):
    """
    Formulario para desvincular a los lideres de grupos de amistad.
    """

    lider = forms.ModelChoiceField(
        queryset=Miembro.objects.all(), label=_lazy('Lider')
    )
    nuevo_lider = forms.ModelChoiceField(
        queryset=Miembro.objects.none(), label=_lazy('Nuevo Lider'),
        required=False
    )

    def __init__(self, iglesia, *args, **kwargs):
        super().__init__(iglesia=iglesia, *args, **kwargs)
        self.fields['lider'].widget.attrs.update({'class': 'form-control'})
        self.fields['nuevo_lider'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['grupo'].required = False

        if self.is_bound:
            lider = self.data.get('lider', None)

            if lider is not None:
                lider = Miembro.objects.get(pk=lider)
                self.fields['nuevo_lider'].queryset = Miembro.objects.lideres_disponibles().filter(
                    grupo__red_id=lider.grupo.red_id)

    def clean(self):
        cleaned_data = super().clean()

        lider = cleaned_data.get('lider', None)
        nuevo_lider = cleaned_data.get('nuevo_lider', None)
        miembros = cleaned_data.get('seleccionados', Miembro.objects.none())
        grupo_destino = cleaned_data.get('grupo_destino', None)

        if lider is not None:
            if lider.grupo_lidera is not None:
                if lider.grupo_lidera.grupos_red.exclude(id=lider.grupo_lidera_id).exists():
                    if nuevo_lider is None:
                        self.add_error('nuevo_lider', forms.ValidationError(
                            forms.Field.default_error_messages['required'], code='required'))
                else:
                    # se va a archivar
                    cleaned_data['grupo'] = lider.grupo_lidera
                    if miembros.exists() and not grupo_destino:
                        self.add_error('grupo_destino', forms.ValidationError(
                            self.error_messages['sin_destino'], code='sin_destino'))

    def desvincular_lider(self):
        """Metodo para desvincular a un lider de un grupo de amistad."""

        lider = self.cleaned_data['lider']
        nuevo_lider = self.cleaned_data.get('nuevo_lider', None)
        grupo = lider.grupo_lidera

        if grupo and not grupo.lideres.count() > 1:
            if not grupo.grupos_red.exclude(id=grupo.id).exists():
                # self.cleaned_data['grupo'] = grupo
                self.cleaned_data['mantener_lideres'] = False
                return self.archiva_grupo()
        elif nuevo_lider is not None and grupo:
            grupo.lideres.add(nuevo_lider)

        lider.update(grupo=None, grupo_lidera=None, estado=Miembro.INACTIVO)
