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
            herbs = Herb.objects.all()
            herb_scores = {herb: herb.get_total_score(selected_diseases) for herb in herbs}
            forbidden_herbs = {herb for herb in herbs if herb.is_forbidden(selected_diseases)}

            # Delete forbidden herbs from recommendations
            for herb in forbidden_herbs:
                herb_scores.pop(herb, None)

            # Sort herbs by score and select top 3
            recommended_herbs = sorted(herb_scores, key=herb_scores.get, reverse=True)[:3]
            recommendations = [(herb.name, herb_scores[herb]) for herb in recommended_herbs]
            neutral_packages = NeutralPackage.objects.all()

            # Create a list of descriptions for forbidden herbs
            forbidden_list = [(herb.name, ', '.join([disease.name for disease in selected_diseases if herb.is_forbidden([disease])])) for herb in forbidden_herbs]

            return render(request, self.success_template_name, {
                'recommendations': recommendations,
                'neutral_packages': neutral_packages,
                'forbidden_list': forbidden_list
            })
        return render(request, self.template_name, {'form': form})
