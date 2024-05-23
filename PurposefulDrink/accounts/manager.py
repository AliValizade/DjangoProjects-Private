from datetime import date
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    '''
    Just essentials informations other fields will be fill in the profile (dashboard part)
    in summary this is our manager for our model user which we useable for create user and craete super user 
    '''
    def create_user(self, phone_number, email, fullname, password, job_pollution_level,
                    job_category, seasonal_allergy, taste_sensitivity, age_category, gender,
                    ):
        if not phone_number:
            raise ValueError('لطفا شماره تلفن خود را وارد نمایید')
        if not email:
            raise ValueError('لطفا ایمیل خود را وارد نمایید')
        if not fullname:
            raise ValueError('لطفا نام و نام خانوادگی خود را وارد نمایید')
        
        #validating email by using normalize_email 
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), fullname = fullname,
                          job_pollution_level=job_pollution_level, job_category=job_category, seasonal_allergy=seasonal_allergy,
                          taste_sensitivity=taste_sensitivity, age_category=age_category, gender=gender)
        user.set_password(password) #using set password for filling password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, fullname, password):
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), fullname=fullname)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser= True
        user.save(using=self._db)
        return user
    
    
    @staticmethod
    def calculate_age(birthdate: date):
        today = date.today()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))