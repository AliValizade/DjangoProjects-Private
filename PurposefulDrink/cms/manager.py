# cms/manager.py
import datetime
from django.db import models
from django.db.models import Sum, When, Case, IntegerField, Q

def calculate_age(birthdate):
    today = datetime.date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

class HerbManager(models.Manager):
    def get_forbidden_herbs(self, user_profile, diseases):
        forbidden_herbs = self.filter_by_disease(diseases)
        forbidden_herbs = self.filter_by_taste(forbidden_herbs, user_profile.taste_sensitivity)
        forbidden_herbs = self.filter_by_age(forbidden_herbs, user_profile.user.date_of_birth)
        forbidden_herbs = self.filter_by_season(forbidden_herbs, user_profile.seasonal_allergy)
        return forbidden_herbs

    def filter_by_disease(self, diseases):
        return self.get_queryset().filter(
            suitability_herb__disease__in=diseases, 
            suitability_herb__score=-100
        ).values_list('id', flat=True).distinct()

    def filter_by_taste(self, queryset, taste_sensitivity):
        if taste_sensitivity:
            return queryset.union(
                self.get_queryset().filter(herb_flavor=taste_sensitivity).values_list('id', flat=True)
            )
        return queryset

    def filter_by_age(self, queryset, date_of_birth):
        from .models import AgeRange
        user_age = calculate_age(date_of_birth)
        inappropriate_age_ranges = AgeRange.objects.filter(
            min_age__lte=user_age, max_age__gte=user_age
        ).values_list('id', flat=True)
        return queryset.union(
            self.get_queryset().filter(
                inappropriate_age_ranges__in=inappropriate_age_ranges
            ).values_list('id', flat=True)
        )

    def filter_by_season(self, queryset, seasonal_allergy):
        current_season = self.get_current_season()
        if seasonal_allergy == current_season:
            return queryset.union(
                self.get_queryset().filter(
                    Q(seasonal_scores__season=current_season) & 
                    Q(seasonal_scores__score__lt=0)
                ).values_list('id', flat=True)
            )
        return queryset

    def get_current_season(self):
        current_month = datetime.datetime.now().month
        if 3 <= current_month <= 5:
            return 'SPRING'
        elif 6 <= current_month <= 8:
            return 'SUMMER'
        elif 9 <= current_month <= 11:
            return 'AUTUMN'
        else:
            return 'WINTER'

    def get_suitable_herbs(self, user_profile, diseases):
        forbidden_herbs = self.get_forbidden_herbs(user_profile, diseases)
        suitable_herbs = self.get_queryset().exclude(
            id__in=forbidden_herbs
        ).annotate(
            total_score=Sum(
                Case(
                    When(suitability_herb__disease__in=diseases,
                         suitability_herb__score__gt=-5,
                         then='suitability_herb__score'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).filter(total_score__gt=0)
        return self.get_final_recommendations(suitable_herbs)

    def get_final_recommendations(self, suitable_herbs):
        herb_scores = {herb.id: herb.total_score for herb in suitable_herbs}
        suitable_herbs = self.remove_interactions(suitable_herbs, herb_scores)

        sorted_herbs = sorted(
            suitable_herbs, 
            key=lambda herb: herb_scores.get(herb.id, 0), 
            reverse=True
        )[:3]

        return [(herb, herb_scores[herb.id]) for herb in sorted_herbs]

    def remove_interactions(self, suitable_herbs, herb_scores):
        for herb in list(suitable_herbs):
            interacting_herbs = herb.interaction_herb.filter(
                id__in=herb_scores.keys()
            )
            for interacting_herb in interacting_herbs:
                if herb_scores.get(interacting_herb.id, 0) >= herb_scores[herb.id]:
                    del herb_scores[herb.id]
                    break
        return suitable_herbs

    def get_suitable_herbs_with_alerts(self, user_profile, selected_diseases):
        suitable_herbs = self.get_suitable_herbs(user_profile, selected_diseases)
        processed_recommendations = []
        for herb, score in suitable_herbs:
            filtered_suitabilities = herb.suitability_herb.filter(
                Q(disease__in=selected_diseases) & 
                Q(alert_states__isnull=False)
            )
            alert_states_set = set(filtered_suitabilities.values_list('alert_states', flat=True))
            processed_recommendations.append((herb, score, alert_states_set))        
        return processed_recommendations
