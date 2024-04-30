from django.db import models

class HerbManager(models.Manager):
    def get_suitable_herbs(self, diseases):
        forbidden_herbs = self.get_queryset().filter(
            suitability_herb__disease__in=diseases, 
            suitability_herb__score=-100
        ).values_list('id', flat=True).distinct()

        return self.get_queryset().exclude(
            id__in=forbidden_herbs
        ).annotate(
            total_score=models.Sum(
                models.Case(
                    models.When(suitability_herb__disease__in=diseases,
                                suitability_herb__score__gt=0,
                                then='suitability_herb__score'),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        ).filter(total_score__gt=0).order_by('-total_score')[:3]
