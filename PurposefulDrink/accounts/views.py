from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import CustomUser , OtpCode
from .forms import UserRegisterForm, UserEditProfileForm, UserLoginForm
from django.contrib import messages
# from utils import send_otp_code
import random
from django.contrib.auth import authenticate, login

# Create your views here.


class LoginRegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_register_form'] = UserRegisterForm()
        context['user_login_form'] = UserLoginForm()
        return context
    def post(self, request):
        user_register_form = UserRegisterForm(request.POST)
        user_login_form = UserLoginForm(request.POST)
        if user_register_form.is_valid():
            cd = user_register_form.cleaned_data
            random_code = random.randint(1000, 9999)
            # send_otp_code(phone_number=cd['phone_number'], code=random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_info'] = {
                'phone_number': cd['phone_number'],
                'fullname': cd['fullname'],
                'email': cd['email'],
                'address': cd['address'],
                'password': cd['password']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify') 
        if user_login_form.is_valid():
            cd = user_login_form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'وارد شدید', 'success')
                return redirect('recommendations')
        return self.render_to_response(self.get_context_data())


class UserProfileView(View):
    form_class = UserEditProfileForm
    temp = 'accounts/profile.html'
    def get(self, request, user_id):
        form = self.form_class
        CustomUser.objects.get(pk=user_id)
        return render(request, self.temp, {'form':form})