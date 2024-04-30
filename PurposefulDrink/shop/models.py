from django.db import models
from django.db.models import Sum, F, Q, Exists, OuterRef

from .manager import HerbManager

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="توضیحات", default='Description')

    def __str__(self) -> str:
        return self.name

class Herb(models.Model):
    # Choose a category (cold or warm)
    TEMPERAMENT_CHOICES = [
        ('COLD', 'سرد'),
        ('HOT', 'گرم'),
    ]
    # Choose the right season
    SEASON_CHOICES = [
        ('SPRING', 'بهار'),
        ('SUMMER', 'تابستان'),
        ('AUTUMN', 'پاییز'),
        ('WINTER', 'زمستان'),
    ]
    NEGATIVE_EFFECT_CHOICES = [
        ('consultation_needed', 'نیاز به مشورت به پزشک دارد'),
        ('contradiction', 'تعارض دارد'),
        ('prohibited', 'قدغن است')
    ]
    name = models.CharField(max_length=100)
    primary_use = models.TextField(verbose_name="کاربرد اصلی")
    negative_effects = models.CharField(max_length=100, choices=NEGATIVE_EFFECT_CHOICES, verbose_name="حالت منفی", null=True, blank=True)
    temperament = models.CharField(max_length=10, choices=TEMPERAMENT_CHOICES, default='COLD', help_text='Select the temperament category of the herb.')
    suitable_season = models.CharField(max_length=10, choices=SEASON_CHOICES, default='SPRING', help_text='Select the suitable season for the herb.')

    objects = HerbManager()

    # @classmethod
    # def get_recommended_herbs(cls, selected_diseases):
    #     return cls.objects.filter(suitability_herb__disease__in=selected_diseases, suitability_herb__score__gt=0).annotate(
    #         total_score=Sum('suitability_herb__score'),
    #         is_forbidden=Exists(Suitability.objects.filter(herb=OuterRef('pk'), disease__in=selected_diseases, score=-100))
    #     ).exclude(is_forbidden=True).order_by('-total_score')[:3]

    def __str__(self) -> str:
        return self.name

class UserDisease(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name="کاربر")
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, verbose_name="بیماری")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        unique_together = ('user', 'disease')  # اطمینان از اینکه هر ترکیب کاربر و بیماری منحصر به فرد است

    def __str__(self):
        return f"{self.user} - {self.disease}"
    
class Suitability(models.Model):
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='suitability_herb')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='suitability_disease')
    score = models.IntegerField()  # 1 to 5 for suitability, -100 for prohibited

    class Meta:
        unique_together = ('herb', 'disease')  # اطمینان از اینکه هر ترکیب گیاه و بیماری منحصر به فرد است

    def __str__(self) -> str:
        return f"{self.herb} Score for {self.disease} is {self.score} "
    
class NeutralPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

