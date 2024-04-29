from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, fullname, address, disease, activity, job, gender, age, password):
        if not phone_number:
            raise ValueError('لطفا شماره تلفن خود را وارد نمایید')
        if not email:
            raise ValueError('لطفا ایمیل خود را وارد نمایید')
        if not fullname:
            raise ValueError('لطفا نام و نام خانوادگی خود را وارد نمایید')
        if not disease:
            raise ValueError('لطفا بیماری مورد نظر را انتخاب نمایید')
        if not activity:
            raise ValueError('لطفا سطح فعالیت خود را انتخاب نمایید')
        if not job:
            raise ValueError('لطفا نوع شغل خود را انتخاب نمایید')
        if not gender:
            raise ValueError('لطفا جنسیت خود را انتخاب نمایید')
        if not age:
            raise ValueError('لطفا سن خود را وارد کنید')
        if not address:
            raise ValueError('لطفا آدرس خود را وارد کنید')
        
        
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), fullname = fullname,
                          disease=disease, activity=activity, job=job, gender=gender, age=age)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, fullname, password):
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), fullname=fullname)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser= True
        user.save(using=self._db)
        return user