from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from cms.models import Disease


def validate_disease_count(value):
    if len(value) > 5:
        raise ValidationError('حداکثر می‌توانید ۵ بیماری انتخاب کنید.')

class DiseaseForm(forms.Form):
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        validators=[validate_disease_count]
    )