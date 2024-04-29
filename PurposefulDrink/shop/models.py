from django.db import models
from django.db.models import Sum, F, Q, Exists, OuterRef


class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Herb(models.Model):
    name = models.CharField(max_length=100)
    
    # Choose a category (cold or warm)
    TEMPERAMENT_CHOICES = [
        ('COLD', 'Cold'),
        ('HOT', 'Hot'),
    ]
    temperament = models.CharField(
        max_length=10,
        choices=TEMPERAMENT_CHOICES,
        default='COLD',
        help_text='Select the temperament category of the herb.'
    )

    # Choose the right season
    SEASON_CHOICES = [
        ('SPRING', 'بهار'),
        ('SUMMER', 'تابستان'),
        ('AUTUMN', 'پاییز'),
        ('WINTER', 'زمستان'),
    ]
    suitable_season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        default='SPRING',
        help_text='Select the suitable season for the herb.'
    )

    @classmethod
    def get_recommended_herbs(cls, selected_diseases):
        return cls.objects.annotate(
            total_score=Sum('suitability_herb__score', filter=Q(suitability_herb__disease__in=selected_diseases) & Q(suitability_herb__score__gt=0)),
            is_forbidden=Exists(Suitability.objects.filter(herb=OuterRef('pk'), disease__in=selected_diseases, score=-100))
        ).exclude(is_forbidden=True).order_by('-total_score')[:3]

    def __str__(self) -> str:
        return self.name


class Suitability(models.Model):
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='suitability_herb')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='suitability_disease')
    herb_properties = models.CharField(max_length=500, blank=True)
    # Three negative states
    NEGATIVE_STATES_CHOICES = [
        ('ALLOWED', 'مجاز است'),
        ('CONSULT', 'نیاز به مشورت به پزشک دارد'),
        ('CONFLICT', 'تعارض دارد'),
        ('FORBIDDEN', 'قدغن است'),
    ]
    negative_states = models.CharField(
        max_length=10,
        choices=NEGATIVE_STATES_CHOICES,
        default='CONSULT',
        help_text='Select the negative state of the herb if applicable.'
    )
    score = models.IntegerField()  # 1 to 5 for suitability, -100 for prohibited

    def __str__(self) -> str:
        return f"{self.herb} Score for {self.disease} is {self.score} "
    

class NeutralPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

