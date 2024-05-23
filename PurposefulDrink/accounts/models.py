from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from cms.models import Disease

# Create your models here.

#TODO Permissions should be fix (second phase)
class User(AbstractBaseUser):
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
    POLLUTION_LEVEL_CHOICES = {
        "LOW": "کم",
        "MEDIUM": "متوسط",
        "MUCH": "زیاد",
        'POLLUTED_JOBS': 'مشاغل آلوده'
    }    
    JOB_TYPE_CHOICES = {
        ('STUDENT', 'دانشجو'),
        ('EMPLOYEE', 'کارمند'),
        ('WORKER', 'کارگر'),
        ('SALESPERSON', 'فروشنده'),
        ('SENSITIVE_JOBS', 'مشاغل حساس'),
        ('HARD_JOBS', 'مشاغل سخت'),
        ('ATHLETE', 'ورزشکار'),
        ('HOUSEKEEPER', 'خانه دار'),
        ('MANAGEMENT', 'مدیریت'),
    }
    GENDER_CHOICE = {
        'Male' : 'مرد',
        'Female': 'زن'
        }
    
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    fullname = models.CharField(max_length=100)
    job_pollution_level = models.CharField(
    max_length=14, choices=POLLUTION_LEVEL_CHOICES, verbose_name="سطج آلودگی شغل", null=True, blank=True
    )    
    job_category = models.CharField(max_length=15, choices=JOB_TYPE_CHOICES, null=True, blank=True)

    seasonal_allergy = models.CharField(
        max_length=10, choices=SEASONAL_ALLERGY_CHOICES, verbose_name="آلرژی فصلی ", null=True, blank=True
    )
    taste_sensitivity = models.CharField(
        max_length=10, choices=TASTE_SENSITIVITY_CHOICES, verbose_name="حساسیت به طعم", null=True, blank=True
    )
    date_of_birth = models.DateField(verbose_name="تاریخ تولد", blank=True, null=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICE)
    address = models.TextField(blank=True, null=True)
    disease = models.ManyToManyField(Disease, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'fullname']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


#TODO Send OtpCode information to Redis DONE

