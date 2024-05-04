from django import forms
from cms.models import Disease

class DiseaseForm(forms.Form):
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
