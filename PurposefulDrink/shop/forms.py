from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from cms.models import Disease

# class AjaxSelectMultipleWidget(forms.SelectMultiple):
#     template_name = 'shop/ajax_select_multiple_widget.html'

#     def __init__(self, url, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.url = url

#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         context['widget']['url'] = self.url
#         return context

def validate_disease_count(value):
    if len(value) > 5:
        raise ValidationError('حداکثر می‌توانید ۵ بیماری انتخاب کنید.')

class DiseaseForm(forms.Form):
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.all(),
        # widget=AjaxSelectMultipleWidget(url=reverse_lazy('disease-ajax-search')),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        validators=[validate_disease_count]
    )