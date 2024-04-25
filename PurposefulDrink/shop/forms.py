from django import forms
from .models import Disease

class DiseaseForm(forms.Form):
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
