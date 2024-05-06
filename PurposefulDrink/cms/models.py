from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from .manager import HerbManager

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="توضیحات", default='Description')

    def __str__(self) -> str:
        return self.name


class AgeRange(models.Model):
    min_age = models.IntegerField(verbose_name="حداقل سن")
    max_age = models.IntegerField(verbose_name="حداکثر سن")

    def __str__(self) -> str:
        return f"{self.min_age} تا {self.max_age} سال"
    

class Herb(models.Model):
    TEMPERAMENT_CHOICES = [
        ('COLD', 'سرد'),
        ('HOT', 'گرم'),
        ('BOTH', 'هردو'),
    ]
    name = models.CharField(max_length=100)
    temperament = models.CharField(max_length=10, choices=TEMPERAMENT_CHOICES, default='COLD', help_text='Select the temperament category of the herb.')
    inappropriate_age_ranges = models.ManyToManyField('AgeRange', verbose_name="بازه‌های سنی نامناسب", blank=True)
    interaction_herb = models.ManyToManyField('self', verbose_name="تداخل گیاهان", blank=True, symmetrical=False)

    objects = HerbManager()

    def __str__(self) -> str:
        return self.name

class SeasonalScore(models.Model):
    SEASON_CHOICES = [
        ('SPRING', 'بهار'),
        ('SUMMER', 'تابستان'),
        ('AUTUMN', 'پاییز'),
        ('WINTER', 'زمستان'),
    ]

    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='seasonal_scores')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    score = models.IntegerField(validators=[MinValueValidator(-3), MaxValueValidator(3)])

    def __str__(self) -> str:
        return f"{self.herb.name} - {self.get_season_display()}"

    class Meta:
        unique_together = ('herb', 'season')


# class HerbInteraction(models.Model):
#     herb1 = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='interactions_herb1')
#     herb2 = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='interactions_herb2')
#     description = models.TextField(verbose_name="توضیح تداخل")

#     class Meta:
#         unique_together = ('herb1', 'herb2')

#     def __str__(self) -> str:
#         return f"تداخل بین {self.herb1.name} و {self.herb2.name}"
    

class UserDisease(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name="کاربر")
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, verbose_name="بیماری")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        unique_together = ('user', 'disease')  # Ensuring that each user and disease combination is unique

    def __str__(self):
        return f"{self.user} - {self.disease}"

def validate_score(value):
    if value not in [1, 2, 3, -100]:
        raise ValidationError('امتیاز باید 1، 2، 3 یا -100 باشد.')
class Suitability(models.Model):
    NEGATIVE_EFFECT_CHOICES = [
        ('consultation_needed', 'نیاز به مشورت به پزشک دارد'),
        ('contradiction', 'تعارض دارد'),
        ('prohibited', 'قدغن است')
    ]
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='suitability_herb')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='suitability_disease')
    negative_effects = models.CharField(max_length=100, choices=NEGATIVE_EFFECT_CHOICES, verbose_name="حالت منفی", null=True, blank=True)
    score = models.IntegerField(validators=[validate_score])  # 1 to 3 for suitability, -100 for prohibited

    class Meta:
        unique_together = ('herb', 'disease')  # Ensuring that each plant and disease combination is unique

    def __str__(self) -> str:
        return f"{self.herb} Score for {self.disease} is {self.score} "
    
class NeutralPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

