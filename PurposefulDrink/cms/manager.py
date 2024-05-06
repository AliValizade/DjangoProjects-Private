from django.db import models
from django.db.models import Sum, When, Case, IntegerField

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

        # Store scores in a dictionary
        herb_scores = {herb.id: herb.total_score for herb in suitable_herbs}

        print('1->', herb_scores)

        # Check for interactions and remove herb with lower scores
        for herb in list(suitable_herbs):
            interacting_herbs = herb.interaction_herb.filter(
                id__in=herb_scores.keys()
            )
            for interacting_herb in interacting_herbs:
                if herb_scores.get(interacting_herb.id, 0) >= herb_scores[herb.id]:
                    del herb_scores[herb.id]
                    break
        # Returning suitable herbs with their scores
        final_recommendations = [
            (herb, herb_scores[herb.id]) for herb in suitable_herbs if herb.id in herb_scores
        ]
        print('2->',final_recommendations)
        
        return final_recommendations
