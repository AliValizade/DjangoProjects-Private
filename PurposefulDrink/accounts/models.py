from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class CustomUser(AbstractBaseUser):
    GENDER_CHOICE = [
        ('male','Male'),
        ('female','Female')
    ]
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    fullname = models.CharField(max_length=100, default=' ')
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICE, default='male')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'fullname']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Information(models.Model):
    """ 
    abstract base class inheritance 
    fields: job, allergy, teste_sensitivity, age_category, job_pollution_level
    """
    SEASONAL_ALLERGY_CHOICES = {
        "SPRING": "بهار",
        "SUMMER": "تابستان",
        "FALL": "پاییز",
        "WINTER": "زمستان"
    }
    TASTE_SENSITIVITY_CHOICES = {
        "SOUR": "ترش", 
        "SWEET": "شیرین",
        "FAST": "تند",
        "BITTER": "تلخ"
    }
    AGE_CATEGORY_CHOICES = {
        "BABY": "خردسال",
        "CHILD": "کودک",
        "TEEN": "نوجوان",
        "ADULT": "جوان",
        "MIDDLE_AGED": "میانسال",
        "ELDER": "سالمند"
    }
    POLLUTION_LEVEL_CHOICES = {
        "LOW": "کم",
        "MEDIUM": "متوسط",
        "MUCH": "زیاد",
        "POLLUTED_JOBS": "مشاغل آلوده",
    }    
    JOB_TYPE_CHOICES = {
        'STUDENT': 'دانشجو',
        'CLERK': 'کارمند',
        'WORKER': 'کارگر',
        'SALESPERSON': 'فروشنده',
        'SENSITIVE_JOBS': 'مشاغل حساس',
        'HARD_JOBS': 'مشاغل سخت',
        'ATHLETE': 'ورزشکار',
        'HOMEMAKER': 'خانه دار',
        'MANAGEMENT': 'مدیریت',
    }
    # TODO: job change create table job normalization db
    job_pollution_level = models.CharField(max_length=13, choices=POLLUTION_LEVEL_CHOICES, verbose_name="سطج آلودگی شغل")    
    job_category = models.CharField(max_length=55, choices=JOB_TYPE_CHOICES, verbose_name="شغل کاربر")
    seasonal_allergy = models.CharField(max_length=10, choices=SEASONAL_ALLERGY_CHOICES, verbose_name="آلرژی فصلی ", null=True, blank=True)
    taste_sensitivity = models.CharField(max_length=10, choices=TASTE_SENSITIVITY_CHOICES, verbose_name="حساسیت به طعم", null=True, blank=True)
    age_category = models.CharField(max_length=11, choices=AGE_CATEGORY_CHOICES, verbose_name="رده سنی ") 

    class Meta:
        abstract = True
        
class Profile(Information):
    """
    user profile + user information
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    
    def __str__(self) -> str:
        return self.user.fullname
        
class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} got the code : {self.code} at {self.created}'
    



