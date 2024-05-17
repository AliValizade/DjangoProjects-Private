from django.views.generic.edit import FormView
from cms.models import Herb
from .forms import DiseaseForm

class RecommendProductsView(FormView):
    template_name = 'shop/index.html'
    form_class = DiseaseForm

    def form_valid(self, form):
        from .models import Product
        selected_diseases = form.cleaned_data['diseases']
        user_profile = self.request.user.profile
        final_recommendations = Herb.objects.get_suitable_herbs_with_alerts(user_profile, selected_diseases)

        product_recommendations = []
        for herb, score, alerts in final_recommendations:
            products = Product.objects.filter(herb=herb)
            for product in products:
                product_recommendations.append((product, score, alerts))


        context = self.get_context_data(form=form)
        context['final_recommendations'] = product_recommendations
        
        return self.render_to_response(context)

    def get_success_url(self):
        return '/success-url/'
