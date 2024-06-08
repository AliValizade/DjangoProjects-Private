from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
# from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User
# Register your models here.
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm

#     list_display = ('pk', 'email', 'phone_number', 'is_admin', 'fullname')
#     list_filter = ('is_admin', )

#     fieldsets = (
#         ('Main', {'fields':('email', 'phone_number', 'fullname', 'password')}),
#         ('Permissions', {'fields':('is_active', 'is_admin')}),
#         ('information', {'fields':('job_pollution_level', 'job_category', 'seasonal_allergy',
#                         'taste_sensitivity', 'gender', 'address', 'disease', 'date_of_birth',)})
#     )


#     add_fieldsets = (
#         ('Main Informations', {'fields':('phone_number', 'email', 'fullname', 'password1', 'password2',)}),
#         ('information', {'fields':('job_pollution_level', 'job_category', 'seasonal_allergy',
#                         'taste_sensitivity', 'date_of_birth', 'gender', 'address', 'disease')})
#     )
#     search_fields = ('email', 'fullname', )
#     ordering = ('fullname', )
#     filter_horizontal = ()

# admin.site.unregister(Group)
admin.site.register(User)
