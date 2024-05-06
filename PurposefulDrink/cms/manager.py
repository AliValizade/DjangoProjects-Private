from django.db import models
from django.db.models import Sum, When, Case, IntegerField, F

class HerbManager(models.Manager):
    def get_suitable_herbs(self, diseases):
        forbidden_herbs = self.get_queryset().filter(
            suitability_herb__disease__in=diseases, 
            suitability_herb__score=-100
        ).values_list('id', flat=True).distinct()

        suitable_herbs = self.get_queryset().exclude(
            id__in=forbidden_herbs
        ).annotate(
            total_score=Sum(
                Case(
                    When(suitability_herb__disease__in=diseases,
                         suitability_herb__score__gt=0,
                         then='suitability_herb__score'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).filter(total_score__gt=0)

        interactions = self.check_herb_interactions(suitable_herbs)
        for herb1, herb2, _ in interactions:
            if herb1.total_score <= herb2.total_score:
                suitable_herbs = suitable_herbs.exclude(id=herb1.id)
            else:
                suitable_herbs = suitable_herbs.exclude(id=herb2.id)

        return suitable_herbs.order_by('-total_score')

    def check_herb_interactions(self, suitable_herbs):
        from .models import HerbInteraction

        interactions = []
        herb_ids_with_scores = suitable_herbs.values_list('id', flat=True)
        for herb_id in herb_ids_with_scores:
            interactions_qs = HerbInteraction.objects.filter(herb1__id=herb_id)
            for interaction in interactions_qs:
                if interaction.herb2.id in herb_ids_with_scores:
                    herb1 = suitable_herbs.get(id=herb_id)
                    herb2 = suitable_herbs.get(id=interaction.herb2.id)
                    interactions.append((herb1, herb2, interaction.description))
        return interactions