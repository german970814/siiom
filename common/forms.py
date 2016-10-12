from django import forms
from django.forms.utils import ErrorList
from django.utils.encoding import force_text
from django.utils.html import format_html_join


class CustomErrorList(ErrorList):

    def __str__(self):
        return self.as_material()

    def as_material(self):
        if not self.data:
            return ''

        return format_html_join('', '<small class="help-block">{}</small>', ((force_text(e),) for e in self))


class CustomModelForm(forms.ModelForm):
    """
    Formulario base para ModelForm.
    """

    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)


class CustomForm(forms.Form):
    """
    Formulario base para Form.
    """

    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)
