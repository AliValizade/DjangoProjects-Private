import datetime
from django.db import models
from django.db.models import Sum, When, Case, IntegerField, Q
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from accounts.manager import UserManager


class DiseaseManager(models.Manager):
    
    def get_by_name(self, name):
        """
        Returns the Disease object with the given name and around disease additional names

        Args:
            name (str): main name or additional name 

        Use Example:
            disease = Disease.objects.get_by_name(name="میگرن")
        Returns:
            Disease or None: The Disease object with the given name, or None if it does not exist.  
        """
        disease = self.get_queryset().filter(name=name).first()
        if disease is None:
            try:
                additional_name = self.get_queryset().filter(additional_name__name=name).first()
                return additional_name
            except ObjectDoesNotExist:
                return None
        else:
            return disease
        

class HerbManager(models.Manager):
    def get_forbidden_herbs(self, user, diseases):
        forbidden_herbs = self.filter_by_disease(diseases)
        forbidden_herbs = self.filter_by_taste(forbidden_herbs, user.taste_sensitivity)
        forbidden_herbs = self.filter_by_age(forbidden_herbs,  UserManager.calculate_age(user.date_of_birth))
        forbidden_herbs = self.filter_by_season(forbidden_herbs, user.seasonal_allergy)
        forbidden_herbs = self.filter_by_job_type(forbidden_herbs, user.job_category)
        forbidden_herbs = self.filter_by_job_type(forbidden_herbs, user.job_pollution_level)
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

    def filter_by_age(self, queryset, user_age):
        from .models import AgeRange
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

    def filter_by_job_type(self, queryset, job_category):
        from .models import JobScore
        if job_category:
            forbidden_herbs_by_job = JobScore.objects.filter(
                job_type=job_category, 
                score=-2
            ).values_list('herb_id', flat=True)
            return queryset.union(forbidden_herbs_by_job)
        return queryset
    
    def filter_by_job_pollution_level(self, queryset, job_pollution_level):
        from .models import JobScore
        if job_pollution_level:
            forbidden_herbs_by_job_pollution_level = JobScore.objects.filter(
                job_pollution=job_pollution_level, 
                score=-2
            ).values_list('herb_id', flat=True)
            return queryset.union(forbidden_herbs_by_job_pollution_level)
        return queryset
    
    def get_suitable_herbs(self, user, diseases):
        forbidden_herbs = self.get_forbidden_herbs(user, diseases)
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
    
    @staticmethod
    def remove_interactions(suitable_herbs, herb_scores):
        # Convert QuerySet to a list to avoid issues with modifying it during iteration
        suitable_herbs_list = list(suitable_herbs)
        
        # Create a copy of the herb_scores dictionary keys to iterate over
        herb_ids = list(herb_scores.keys())

        for herb_id in herb_ids:
            # Get the herb object for the current herb_id
            herb = next((herb for herb in suitable_herbs_list if herb.id == herb_id), None)
            if not herb:
                continue
            
            interacting_herbs = herb.interaction_herb.filter(id__in=herb_scores.keys())

            for interacting_herb in interacting_herbs:
                interacting_herb_id = interacting_herb.id
                if herb_scores.get(interacting_herb_id, 0) >= herb_scores.get(herb_id, 0):
                    herb_scores.pop(herb_id, None)
                    break  # Exit the inner loop to avoid further comparison
                else:
                    herb_scores.pop(interacting_herb_id, None)

        # Filter the suitable_herbs based on the remaining herb_scores keys
        remaining_herb_ids = herb_scores.keys()
        suitable_herbs = [herb for herb in suitable_herbs_list if herb.id in remaining_herb_ids]
        
        return suitable_herbs
    
    @staticmethod
    def get_current_season():
        current_month = datetime.datetime.now().month
        if 3 <= current_month <= 5:
            return 'SPRING'
        elif 6 <= current_month <= 8:
            return 'SUMMER'
        elif 9 <= current_month <= 11:
            return 'AUTUMN'
        else:
            return 'WINTER'
    