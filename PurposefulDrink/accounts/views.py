from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import User
from .forms import UserRegisterForm, UserLoginForm, VefiyCodeForm, UserEditProfileForm
from django.contrib import messages
from utils import OtpManager, RedisManager
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core import serializers
from cms.models import Disease
import json
# Create your views here.


class LoginRegisterView(TemplateView):
    template_name = 'accounts/register.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_register_form'] = UserRegisterForm
        context['user_login_form'] = UserLoginForm
        return context
    def post(self, request):
        user_register_form = UserRegisterForm(request.POST)
        user_login_form = UserLoginForm(request.POST)
        if user_register_form.is_valid():
            # TODO: CHECK USER phone_number It already exists or not ? 
            cd = user_register_form.cleaned_data
            if User.objects.filter(phone_number=cd['phone_number']).exists():
                messages.ERROR(request, 'شماره تلفن تکراری می باشد', 'warning')
                return redirect('accounts:loginregister')
            else:
                code = OtpManager.generate_otp_code()
                OtpManager().send_otp_code(code)
                RedisManager().add_to_redis(cd['phone_number'], code)
                print('=' * 80)
                print(cd ['disease'])
                print(type(cd['disease']))
                serialized_disease = serializers.serialize('json', cd['disease'])
                deserialized_disease = json.loads(serialized_disease)
                disease_names = [item['fields']['name'] for item in deserialized_disease]
                print(disease_names)
                print(serialized_disease)
                # print(disease_names)
                request.session['user_info'] = {
                    'phone_number': cd['phone_number'],
                    'fullname': cd['fullname'],
                    'email': cd['email'],
                    'password': cd['password'],
                    'job_pollution_level': cd['job_pollution_level'],
                    'job_category': cd['job_category'],
                    'seasonal_allergy': cd['seasonal_allergy'],
                    'taste_sensitivity': cd['taste_sensitivity'],
                    'age_category': cd['age_category'],
                    'gender': cd['gender'],
                    'disease': disease_names
                }
                messages.success(request, 'we sent you a code', 'success')
                print('=' * 80)
                print(code)
                return redirect('accounts:verify') 
        if user_login_form.is_valid():
            cd = user_login_form.cleaned_data
            user = authenticate(phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'وارد شدید', 'success')
                return redirect('shop:recommended_products')
        return self.render_to_response(self.get_context_data())




class VerifyOtpCode(View):
    form_class = VefiyCodeForm
    temp = 'accounts/verify.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.temp, {'form':form})

    def post(self, request):
        user_session = request.session['user_info']
        code_instance = RedisManager().get_by_redis(user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if str(cd['code']) == str(code_instance):
                new_user =User.objects.create_user(phone_number=user_session['phone_number'], email=user_session['email'],
                                         fullname=user_session['fullname'], password=user_session['password'],
                                         job_pollution_level=user_session['job_pollution_level'], job_category=user_session['job_category'],
                                         seasonal_allergy=user_session['seasonal_allergy'], taste_sensitivity=user_session['taste_sensitivity'],
                                         age_category=user_session['age_category'], gender=user_session['gender'],)
                diseases = Disease.objects.filter(name__in=user_session['disease'])
                print('8' * 100)
                new_user.disease.set(diseases)
                messages.success(request, 'You Registred', 'success')
                return redirect('cms:cmsview')
            else:
                messages.error(request, 'Wrong code', 'danger')
                return redirect('accounts:verify')
        return render(request, self.temp, {'form':form})


class UserProfileView(View):
     form_class = UserEditProfileForm
     temp = 'accounts/profile.html'
     def get(self, request, user_id):
         form = self.form_class
         User.objects.get(pk=user_id)
         return render(request, self.temp, {'form':form})
    
     def post(self, request, user_id):
         user = User.objects.get(pk=user_id)
         form = self.form_class(request.POST, instance=user)
         if form.is_valid():
            form.save()
            return redirect('cms:cmsview')
    
         return render(request, self.temp, {'form':form})
     

class UserLogoutView(View):
    def get(self, reqeust):
        pass


class UserPasswordResetView(View):
    pass


class UserPasswordResetDoneView(View):
    pass

class UserConfirmPasswordResetView(View):
    pass

class UserPasswordResetCompleteView(View):
    pass