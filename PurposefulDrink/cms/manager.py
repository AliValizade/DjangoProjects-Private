import datetime
from django.db import models
from django.db.models import Sum, When, Case, IntegerField, Q, OuterRef, Subquery, F, Value
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
        forbidden_herbs = self.filter_by_job_pollution_level(forbidden_herbs, user.job_pollution_level)
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

    def filter_by_season(self, queryset, user_seasonal_allergy):
        current_season = self.get_current_season()
        
        forbidden_by_allergy = self.get_queryset().filter(
            seasonal_scores__season=current_season,
            seasonal_scores__allergy_aggravator='YES'
        ).values_list('id', flat=True)
        print("forbidden_by_allergy: ", list(forbidden_by_allergy))

        forbidden_by_season_score = self.get_queryset().filter(
            seasonal_scores__season=current_season,
            seasonal_scores__score=-100
        ).values_list('id', flat=True)
        print("forbidden_by_season_score: ", list(forbidden_by_season_score))

        if user_seasonal_allergy == current_season:
            queryset = queryset.union(forbidden_by_allergy)
        
        queryset = queryset.union(forbidden_by_season_score)
        
        return queryset

    def filter_by_job_type(self, queryset, job_category):
        from .models import JobScore
        if job_category:
            forbidden_herbs_by_job = JobScore.objects.filter(
                job_type=job_category, 
                score=-100
            ).values_list('herb_id', flat=True)
            return queryset.union(forbidden_herbs_by_job)
        return queryset
    
    def filter_by_job_pollution_level(self, queryset, job_pollution_level):
        from .models import JobPollutionLevelScore
        if job_pollution_level:
            forbidden_herbs_by_job_pollution_level = JobPollutionLevelScore.objects.filter(
                job_pollution=job_pollution_level, 
                score=-100
            ).values_list('herb_id', flat=True)
            return queryset.union(forbidden_herbs_by_job_pollution_level)
        return queryset
    
    def get_suitable_herbs(self, user, diseases):
        from .models import SeasonalScore, JobScore

        forbidden_herbs = self.get_forbidden_herbs(user, diseases)

        # Calculate the treatment priority score for the disease
        suitability_scores = self.get_queryset().filter(
            suitability_herb__disease__in=diseases,
            suitability_herb__score__gt=-5
        ).exclude(id__in=forbidden_herbs).annotate(
            suitability_score=Sum('suitability_herb__score')
        )

        # Calculate seasonal score using Subquery
        seasonal_scores_subquery = SeasonalScore.objects.filter(
            herb=OuterRef('pk'),
            score__gt=-100
        ).values('herb').annotate(
            total_seasonal_score=Sum('score')
        ).values('total_seasonal_score')

        # Calculate Job_type score using Subquery
        job_scores_subquery = JobScore.objects.filter(
            herb=OuterRef('pk'),
            score__gt=-100
        ).values('herb').annotate(
            total_job_type_score=Sum('score')
        ).values('total_job_type_score')

        suitable_herbs = suitability_scores.annotate(
            job_type_score=Subquery(job_scores_subquery, output_field=IntegerField(), default=Value(0)),
            seasonal_score=Subquery(seasonal_scores_subquery, output_field=IntegerField(), default=Value(0)),
            total_score=F('suitability_score') + F('seasonal_score') + F('job_type_score')
        ).filter(total_score__gt=0)

        print('suit-1: ==>', suitable_herbs)

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
        current_date = datetime.datetime.now()
        current_month = current_date.month
        current_day = current_date.day
        
        if (current_month == 3 and current_day >= 20) or (current_month == 4) or (current_month == 5) or (current_month == 6 and current_day < 21):
            return 'SPRING'
        elif (current_month == 6 and current_day >= 21) or (current_month == 7) or (current_month == 8) or (current_month == 9 and current_day < 22):
            return 'SUMMER'
        elif (current_month == 9 and current_day >= 22) or (current_month == 10) or (current_month == 11) or (current_month == 12 and current_day < 21):
            return 'AUTUMN'
        else:
            return 'WINTER'
    