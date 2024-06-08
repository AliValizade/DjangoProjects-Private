from django.db import models
from django.urls import reverse
from django.forms import ValidationError
from cms.manager import DiseaseManager, HerbManager



class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام بیماری")

    objects = DiseaseManager()
    
    def __str__(self) -> str:
        return self.name
    
    class Meta: 
        indexes = [
            models.Index(fields=['name'])
        ]

class AdditionalName(models.Model):
    disease = models.ForeignKey("Disease", on_delete=models.CASCADE, related_name="additional_name")
    name = models.CharField(max_length=100,unique=True, verbose_name="نام اضافی")
    
    def __str__(self) -> str:
        return self.name
    
    class Meta: 
        verbose_name = "Add Names Disease"


class AgeRange(models.Model):
    CATEGORY_CHOICES = [
        ('BABY', 'خردسال'),
        ('CHILD', 'کودک'),
        ('TEEN', 'نوجوان'),
        ('ADULT', 'جوان'),
        ('MIDDLE_AGED', 'میانسال'),
        ('ELDER', 'سالمند'),
    ]
    min_age = models.IntegerField(verbose_name="حداقل سن")
    max_age = models.IntegerField(verbose_name="حداکثر سن")
    name = models.CharField(choices=CATEGORY_CHOICES, max_length=20, verbose_name="نام رده سنی")
    
    def __str__(self) -> str:
        return f"{self.name}=>{self.min_age} - {self.max_age} سال"


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


class JobScore(models.Model):
    JOB_TYPE_CHOICES = (
        ('STUDENT', 'دانشجو'),
        ('EMPLOYEE', 'کارمند'),
        ('WORKER', 'کارگر'),
        ('SALESPERSON', 'فروشنده'),
        ('SENSITIVE_JOBS', 'مشاغل حساس'),
        ('HARD_JOBS', 'مشاغل سخت'),
        ('ATHLETE', 'ورزشکار'),
        ('HOUSEKEEPER', 'خانه دار'),
        ('MANAGEMENT', 'مدیریت'),
    )
    SCORE_CHOICES = [
        (1, 'خوب'),
        (0, 'خنثی'),
        (-1, 'توصیه نمیشود'),
        (-100, 'قدغن است'),
    ]
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='job_scores')
    job_type = models.CharField(max_length=14, choices=JOB_TYPE_CHOICES)
    score = models.IntegerField(choices=SCORE_CHOICES)

    def __str__(self) -> str:
        return f"{self.herb.name} - {self.score}"

    class Meta:
        unique_together = ('herb', 'job_type')


class JobPollutionLevelScore(models.Model):
    POLLUTION_LEVEL_CHOICES = {
        "LOW": "کم",
        "MEDIUM": "متوسط",
        "MUCH": "زیاد",
        'POLLUTED_JOBS': 'مشاغل آلوده'
    }
    SCORE_CHOICES = [
        (1, 'خوب'),
        (0, 'خنثی'),
        (-1, 'توصیه نمیشود'),
        (-100, 'قدغن است'),
    ]
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='pollution_scores')
    job_pollution = models.CharField(max_length=14, choices=POLLUTION_LEVEL_CHOICES)
    score = models.IntegerField(choices=SCORE_CHOICES)

    def __str__(self) -> str:
        return f"{self.herb.name} - {self.score}"

    class Meta:
        unique_together = ('herb', 'job_pollution')


class SeasonalScore(models.Model):
    SEASON_CHOICES = [
        ('SPRING', 'بهار'),
        ('SUMMER', 'تابستان'),
        ('AUTUMN', 'پاییز'),
        ('WINTER', 'زمستان'),
    ]
    SCORE_CHOICES = [
        (3, 'اولویت اول'),
        (2, 'اولویت دوم'),
        (1, 'اولویت سوم'),
        (-1, 'توصیه نمیشود'),
        (-100, 'قدغن است'),
    ]
    ALLERGY_AGGRAVATOR_CHOISE = [
        ('YES', 'بله'),
        ('NO', 'خیر'),
    ]
    herb = models.ForeignKey(Herb, on_delete=models.CASCADE, related_name='seasonal_scores')
    season = models.CharField(max_length=10, verbose_name='فصل', choices=SEASON_CHOICES)
    allergy_aggravator = models.CharField(max_length=3, verbose_name='تشدیدکننده ی  آلرژی فصلی', choices=ALLERGY_AGGRAVATOR_CHOISE, default='NO')
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name='اولویت درمان')

    def __str__(self) -> str:
        return f"{self.herb.name} - {self.get_season_display()}"

    class Meta:
        unique_together = ('herb', 'season')


def validate_score(value):
    if value not in [1, 2, 3, -100]:
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
    ]
    herb = models.ForeignKey(Herb, verbose_name='گیاه', on_delete=models.CASCADE, related_name='suitability_herb')
    disease = models.ForeignKey(Disease, verbose_name='بیماری', on_delete=models.CASCADE, related_name='suitability_disease')
    alert_states = models.CharField(max_length=100, choices=ALERT_STATES_CHOICES, verbose_name="حالات هشدار", null=True, blank=True)
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name='اولویت درمان')  # 1 to 3 for suitability, -100 for prohibited

    class Meta:
        unique_together = ('herb', 'disease')  # Ensuring that each plant and disease combination is unique

    def __str__(self):
        return f"{self.herb} Score for {self.disease} is {self.score} "

