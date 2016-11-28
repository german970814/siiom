# Django
from django import forms

# Apps
from .models import Encuentro, Encontrista

from common.forms import CustomModelForm, CustomForm
from grupos.models import Grupo, Red
from miembros.models import Miembro


class CrearEncuentroForm(CustomModelForm):
    """
    Formulario para crear encuentros
    """

    red = forms.ModelChoiceField(queryset=Red.objects.all())

    class Meta:
        model = Encuentro
        fields = (
            'fecha_inicial', 'fecha_final', 'hotel',
            'grupos', 'coordinador', 'tesorero',
            'direccion', 'observaciones',
        )  # se agrega fields
        # exclude = ('dificultades', 'estado')  # se comenta el exclude

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupos'].queryset = Grupo.objects.none()  # prefetch_related('lideres').all()
        self.fields['coordinador'].queryset = Miembro.objects.none()
        self.fields['tesorero'].queryset = Miembro.objects.none()
        self.fields['fecha_inicial'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00 00:00'})
        self.fields['fecha_final'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})
        self.fields['coordinador'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['red'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['tesorero'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['observaciones'].widget.attrs.update({'class': 'form-control', 'rows': '5'})
        self.fields['grupos'].widget.attrs.update(
            {
                'class': 'selectpicker',
                'data-live-search': 'true',
                'data-actions-box': 'true',
                # 'multiple data-selected-text-format': 'count',
                'liveSearchPlaceholder': 'Busca por nombre de líder',
                'noneSelectedText': 'SIN ESCOGER'
            }
        )
        self.fields['hotel'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})

        if self.is_bound:
            red = self.data.get('red', None) or None
            grupos = self.data.get('grupo', None) or None

            if red is not None:
                try:
                    red = Red.objects.get(id=red)
                    self.fields['grupos'].queryset = Grupo.objects.filter(red=red).prefetch_related('lideres')
                except Red.DoesNotExist:
                    self.fields['grupos'].queryset = Grupo.objects.none()
            else:
                self.fields['grupos'].queryset = Grupo.objects.none()

            queryset_miembros = Miembro.objects.none()
            if grupos is not None:
                grupos = Grupo.objects.filter(id__in=grupos)
                if grupos.exists():
                    _ids_miembros = grupos.values_list('lideres__id', flat=True)
                    queryset_miembros = Miembro.objects.filter(id__in=_ids_miembros)

            self.fields['tesorero'].queryset = queryset_miembros
            self.fields['coordinador'].queryset = queryset_miembros

            # try:
            #     tesorero = self.data.get('tesorero', None)
            #     coordinador = self.data.get('coordinador', None)
            #     queryset_tesorero = Miembro.objects.filter(id=tesorero)
            #     queryset_coordinador = Miembro.objects.filter(id=coordinador)
            # except:
            #     queryset_tesorero = Miembro.objects.none()
            #     queryset_coordinador = Miembro.objects.none()
            # self.fields['tesorero'].queryset = queryset_tesorero
            # self.fields['coordinador'].queryset = queryset_coordinador


class NuevoEncontristaForm(forms.ModelForm):
    """
    Formulario Para la Creacion de Encontristas
    """
    error_css_class = 'has-error'

    class Meta:
        model = Encontrista
        exclude = ('encuentro', )

    def __init__(self, encuentro=None, *args, **kwargs):
        super(NuevoEncontristaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        if encuentro:
            self.fields['grupo'].queryset = Grupo.objects.none()
        else:
            self.fields['grupo'].queryset = Grupo.objects.filter(id=self.instance.grupo.id)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['genero'].widget.attrs.update({'class': 'selectpicker'})

        if self.is_bound:
            try:
                grupo = self.data.get('grupo', None)
                queryset = Grupo.objects.filter(id=grupo)
            except:
                queryset = Grupo.objects.none()
            self.fields['grupo'].queryset = queryset


class EditarEncuentroForm(CrearEncuentroForm):
    def __init__(self, *args, **kwargs):
        super(EditarEncuentroForm, self).__init__(*args, **kwargs)
        self.fields['coordinador'].widget.attrs.update({'readonly': ''})
        self.fields['tesorero'].widget.attrs.update({'readonly': ''})

        if not self.is_bound:
            if self.instance:
                if any(self.instance.grupos.all()):
                    self.fields['red'].initial = self.instance.grupos.first().red

                self.fields['coordinador'].queryset = Miembro.objects.filter(id=self.instance.coordinador.id)
                self.fields['coordinador'].initial = self.instance.coordinador

                self.fields['tesorero'].queryset = Miembro.objects.filter(id=self.instance.tesorero.id)
                self.fields['tesorero'].initial = self.instance.tesorero


class FormularioObtenerGrupoAPI(CustomForm):
    """Formulario para el uso desde la api, para obtener grupos"""
    red = forms.ModelChoiceField(queryset=Red.objects.all())
    value = forms.CharField(max_length=255)
