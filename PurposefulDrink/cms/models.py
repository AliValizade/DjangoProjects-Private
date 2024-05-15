from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from .manager import HerbManager

class Disease(models.Model):
    name = models.CharField(verbose_name='نام بیماری', max_length=100)
    similar_names = ArrayField(models.CharField(max_length=100), verbose_name="نام‌های مشابه", blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class AgeRange(models.Model):
    min_age = models.IntegerField(verbose_name="حداقل سن")
    max_age = models.IntegerField(verbose_name="حداکثر سن")

    def __str__(self) -> str:
        return f"{self.min_age} - {self.max_age} سال"


class Herb(models.Model):
    TEMPERAMENT_CHOICES = [
        ('COLD', 'سرد'),
        ('HOT', 'گرم'),
        ('BOTH', 'هردو'),
    ]
    HERB_FLAVOR_CHOICES = {
        ("SOUR", "ترش"), 
        ("SWEET", "شیرین"),
        ("FAST", "تند"),
        ("BITTER", "تلخ"),
    }
    name = models.CharField(verbose_name='نام گیاه', max_length=100)
    herb_flavor = models.CharField(verbose_name='مزه گیاه', max_length=10, choices=HERB_FLAVOR_CHOICES, blank=True, help_text='Select the flavor of the herb.')
    temperament = models.CharField(verbose_name='طبع گیاه', max_length=10, choices=TEMPERAMENT_CHOICES, default='COLD', help_text='Select the temperament category of the herb.')
    inappropriate_age_ranges = models.ManyToManyField('AgeRange', verbose_name="بازه‌های سنی نامناسب", blank=True)
    interaction_herb = models.ManyToManyField('self', verbose_name="تداخل گیاهان", blank=True, symmetrical=True)

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

    herb = models.ForeignKey(Herb, verbose_name='گیاه', on_delete=models.CASCADE, related_name='seasonal_scores')
    season = models.CharField(verbose_name='فصل', max_length=10, choices=SEASON_CHOICES)
    score = models.IntegerField(validators=[MinValueValidator(-3), MaxValueValidator(3)])

    def __str__(self) -> str:
        return f"{self.herb.name} - {self.get_season_display()}"

    class Meta:
        unique_together = ('herb', 'season')


class UserDisease(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name="کاربر")
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE, verbose_name="بیماری")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        unique_together = ('user', 'disease')  # Ensuring that each user and disease combination is unique

    def __str__(self):
        return f"{self.user} - {self.disease}"


def validate_score(value):
    if value not in [1, 2, 3, -1, -100]:
        raise ValidationError('امتیاز باید 1، 2، 3 یا -1 و -100 باشد.')
class Suitability(models.Model):
    SCORE_CHOICES = [
        (3, 'درمان اول'),
        (2, 'درمان دوم'),
        (1, 'درمان سوم'),
        (-1, 'توصیه نمیشود'),
        (-100, 'قدغن است'),
    ]
    ALERT_STATES_CHOICES = [
        ('consultation_needed', 'نیاز به مشورت به پزشک دارد'),
        ('contradiction', 'تعارض دارد'),
    ]
    herb = models.ForeignKey(Herb, verbose_name='گیاه', on_delete=models.CASCADE, related_name='suitability_herb')
    disease = models.ForeignKey(Disease, verbose_name='بیماری', on_delete=models.CASCADE, related_name='suitability_disease')
    alert_states = models.CharField(max_length=100, choices=ALERT_STATES_CHOICES, verbose_name="حالات هشدار", null=True, blank=True)
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name='اولویت درمان')  # 1 to 3 for suitability, -100 for prohibited

    class Meta:
        unique_together = ('herb', 'disease')  # Ensuring that each plant and disease combination is unique

    def __str__(self) -> str:
        return f"{self.herb} Score for {self.disease} is {self.score} "

    
class NeutralPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

