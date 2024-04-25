from django.db import models
from django.db.models import Sum

class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Herb(models.Model):
    name = models.CharField(max_length=100)
    
    # Choose a category (cold or warm)
    TEMPERATURE_CHOICES = [
        ('COLD', 'Cold'),
        ('HOT', 'Hot'),
    ]
    temperature = models.CharField(
        max_length=10,
        choices=TEMPERATURE_CHOICES,
        default='COLD',
        help_text='Select the temperature category of the herb.'
    )

    # Choose the right season
    SEASON_CHOICES = [
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('AUTUMN', 'Autumn'),
        ('WINTER', 'Winter'),
    ]
    suitable_season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        default='SPRING',
        help_text='Select the suitable season for the herb.'
    )

    # Choose the age category
    AGE_GROUP_CHOICES = [
        ('INFANT', 'Infant'),
        ('CHILD', 'Child'),
        ('TEEN', 'Teen'),
        ('ADULT', 'Adult'),
        ('MIDDLE_AGED', 'Middle Aged'),
        ('SENIOR', 'Senior'),
    ]
    age_group = models.CharField(
        max_length=15,
        choices=AGE_GROUP_CHOICES,
        default='ADULT',
        help_text='Select the suitable age group for the herb.'
    )

    def get_total_score(self, diseases):
        """Calculate the total score for the herb based on the given diseases."""
        total_score = Suitability.objects.filter(
            herb=self, 
            disease__in=diseases,
            score__gt=0
        ).aggregate(total_score=Sum('score'))['total_score']
        # print(total_score)
        return total_score or 0

    def is_forbidden(self, diseases):
        """Check if the herb is forbidden for any of the given diseases."""
        return Suitability.objects.filter(herb=self, disease__in=diseases).filter(score=-100).exists()

    def __str__(self) -> str:
        return self.name


class Suitability(models.Model):
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    score = models.IntegerField()  # 1 to 5 for suitability, -100 for prohibited

    def __str__(self) -> str:
        return f"{self.herb} Score for {self.disease} is {self.score} "
    

class NeutralPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

