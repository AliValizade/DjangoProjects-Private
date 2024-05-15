from django.views.generic.edit import FormView
from django.db.models import Q
from django.http import JsonResponse

from cms.models import Herb, Suitability, Disease
from .forms import DiseaseForm

class RecommendHerbsView(FormView):
    template_name = 'shop/index.html'
    form_class = DiseaseForm

    def form_valid(self, form):
        selected_diseases = form.cleaned_data['diseases']
        # diseases = self.search_diseases(selected_diseases)

        user_profile = self.request.user.profile
        
        final_recommendations = Herb.objects.get_suitable_herbs(user_profile, selected_diseases)
        
        context = self.get_context_data(form=form)
        context['final_recommendations'] = final_recommendations
        
        return self.render_to_response(context)
    
    # def search_diseases(self, query):
    #     # Search for original name or similar names
    #     return Disease.objects.filter(
    #         Q(name__icontains=query) | Q(similar_names__icontains=query)
    #     )

    def get_success_url(self):
        return '/success-url/'


# def ajax_search_view(request):
#     query = request.GET.get('query', '')
#     diseases = Disease.objects.filter(name__icontains=query)
#     results = [{'id': disease.id, 'name': disease.name} for disease in diseases]
#     return JsonResponse(results, safe=False)