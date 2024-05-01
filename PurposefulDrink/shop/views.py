from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.db.models import Sum, Case, When, IntegerField
from django.urls import reverse_lazy
from .models import Herb, Suitability
from .forms import DiseaseForm

class RecommendHerbsView(FormView):
    template_name = 'shop/index.html'
    form_class = DiseaseForm
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        selected_diseases = form.cleaned_data['diseases']
        herbs = Herb.objects.get_suitable_herbs(selected_diseases)
        context['herbs'] = herbs

        forbidden_herbs = Suitability.objects.filter(
            disease__in=selected_diseases, score=-100
        ).select_related('herb', 'disease').order_by('herb__name')

        context['forbidden_herbs'] = [
            (item.herb.name, item.disease.name) for item in forbidden_herbs
        ]

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['herbs'] = []
        return context