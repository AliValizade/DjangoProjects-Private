from django.db.models import Sum, F, Q, Exists, OuterRef
from django.views import View
from django.shortcuts import render
from .models import Herb, Disease, Suitability, NeutralPackage
from .forms import DiseaseForm

class RecommendHerbsView(View):
    form_class = DiseaseForm
    template_name = 'shop/index.html'
    success_template_name = 'shop/recommend.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            selected_diseases = form.cleaned_data['diseases']
            recommended_herbs = Herb.get_recommended_herbs(selected_diseases)
            recommendations = [(herb.name, herb.total_score) for herb in recommended_herbs]
            neutral_packages = NeutralPackage.objects.all()


            
            # Check if all recommended herbs have a total_score of 0 or None
            if all(score is None or score == 0 for _, score in recommendations):
                # Only show neutral packages if no valid recommendations exist
                return render(request, self.success_template_name, {
                    'neutral_packages': neutral_packages,
                    'recommendations': None
                })

            all_forbidden_suitabilities = Suitability.objects.filter(
            disease__in=selected_diseases,
            score=-100
            ).select_related('herb').all()

            forbidden_herbs_dict = {suitability.herb.id: suitability.herb for suitability in all_forbidden_suitabilities}

            forbidden_list = [
                (forbidden_herbs_dict[herb_id].name, ', '.join([disease.name for disease in selected_diseases]))
                for herb_id in forbidden_herbs_dict
            ]

            return render(request, self.success_template_name, {
                'recommendations': recommendations,
                'neutral_packages': neutral_packages,
                'forbidden_list': forbidden_list
            })
        return render(request, self.template_name, {'form': form})
