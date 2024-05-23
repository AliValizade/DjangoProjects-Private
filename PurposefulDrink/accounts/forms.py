from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    '''
    This is a form for create user in admin panel and it use for compeleteing user informations
    
    '''
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'fullname')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('پسورد ها باید همسان باشند')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    '''
    for editing user information on admin panel 
    
    '''
    password = ReadOnlyPasswordHashField(help_text= 'you can change password by using <a href=\"../password/\"> this form</a>. ')
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'fullname')




class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    class Meta:
        model = User
        exclude = ['is_admin', 'is_active', 'address', 'last_login']
        widget  = {
            'disease': forms.MultipleChoiceField()
        }

       
class VefiyCodeForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'شماره تلفن'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'رمز عبور'}))
    
class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'job_pollution_level', 'job_category', 'seasonal_allergy',
                  'taste_sensitivity', 'date_of_birth', 'gender', 'address', 'disease')