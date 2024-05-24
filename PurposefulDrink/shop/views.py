from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from django.db.models import Count

from cms.models import Herb
from cms.forms import DiseaseForm

class ShopView(View):
    pass

class RecommendProductsView(FormView):
    template_name = 'shop/index.html'
    form_class = DiseaseForm

    def form_valid(self, form):
        from .models import Product
        selected_diseases = form.cleaned_data['diseases']
        user = self.request.user
        final_recommendations = Herb.objects.get_suitable_herbs_with_alerts(user, selected_diseases)

        herb_ids = [herb.id for herb, _, _ in final_recommendations]

        # Filter products with herb count 1
        products = Product.objects.annotate(herb_count=Count('herbs')).filter(
            herb_count__lte=1,
            herbs__in=herb_ids
        ).distinct().prefetch_related('herbs')

        product_recommendations = []
        for product in products:
            for id, (herb, score, alerts) in enumerate(final_recommendations):
                if herb in product.herbs.all():
                    treatment_label = ''
                    if id == 0:
                        treatment_label = 'درمان اول'
                    elif id == 1:
                        treatment_label = 'درمان دوم'
                    elif id == 2:
                        treatment_label = 'درمان سوم'
                    product_recommendations.append((product, treatment_label, alerts))

        # Sort the final recommendations by the treatment label
        treatment_order = {'درمان اول': 1, 'درمان دوم': 2, 'درمان سوم': 3}
        product_recommendations.sort(key=lambda x: treatment_order[x[1]])
        
        context = self.get_context_data(form=form)
        context['final_recommendations'] = product_recommendations
        
        return self.render_to_response(context)

    def get_success_url(self):
        return '/success-url/'