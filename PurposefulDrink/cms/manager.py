import datetime
from django.db import models
from django.db.models import Sum, When, Case, IntegerField, Q

class HerbManager(models.Manager):
    def get_suitable_herbs(self, user_profile, diseases):
        from .models import AgeCategory
        forbidden_herbs = self.get_queryset().filter(
            suitability_herb__disease__in=diseases, 
            suitability_herb__score=-100
        ).values_list('id', flat=True).distinct()

        # Filter herbs based on the user's taste sensitivity
        if user_profile.taste_sensitivity:
            forbidden_herbs = forbidden_herbs.union(
                self.get_queryset().filter(herb_flavor=user_profile.taste_sensitivity).values_list('id', flat=True)
            )

        # Filter plants based on the user's age category
        if user_profile.age_category:
            inappropriate_age_ranges_ids = AgeCategory.objects.filter(
                category=user_profile.age_category
            ).values_list('id', flat=True)
            forbidden_herbs = forbidden_herbs.union(
                self.get_queryset().filter(
                    inappropriate_age_ranges__in=inappropriate_age_ranges_ids
                ).values_list('id', flat=True)
            )

        # Determine the current season based on the system date
        current_month = datetime.datetime.now().month
        if 3 <= current_month <= 5:
            current_season = 'SPRING'
        elif 6 <= current_month <= 8:
            current_season = 'SUMMER'
        elif 9 <= current_month <= 11:
            current_season = 'AUTUMN'
        else:
            current_season = 'WINTER'
        
        # Filter herbs based on the user's seasonal sensitivity and the herb's seasonal rating
        if user_profile.seasonal_allergy == current_season:
            forbidden_herbs = forbidden_herbs.union(
                self.get_queryset().filter(
                    Q(seasonal_scores__season=current_season) & 
                    Q(seasonal_scores__score__lt=0)
                ).values_list('id', flat=True)
            )

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
        
        return final_recommendations
