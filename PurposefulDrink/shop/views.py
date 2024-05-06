from django.views.generic.edit import FormView
from cms.models import Herb, Suitability
from .forms import DiseaseForm

class RecommendHerbsView(FormView):
    template_name = 'shop/index.html'
    form_class = DiseaseForm

    def form_valid(self, form):
        selected_diseases = form.cleaned_data['diseases']
        user_profile = self.request.user.profile
        
        final_recommendations = Herb.objects.get_suitable_herbs(user_profile, selected_diseases)
        
        forbidden_herbs = Suitability.objects.filter(
            disease__in=selected_diseases, score=-100
        ).select_related('herb', 'disease').order_by('herb__name')
        
        # forbidden_herb_list = [
        #     (item.herb.name, item.disease.name) for item in forbidden_herbs
        # ]

        # user_profile = self.request.user.profile
        # recommendations = user_profile.get_recommendations()

        context = self.get_context_data(form=form)
        context['final_recommendations'] = final_recommendations
        # context['forbidden_herbs'] = forbidden_herb_list
        # context['recommendations'] = recommendations

        return self.render_to_response(context)

    def get_success_url(self):
        return '/success-url/'
