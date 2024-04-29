from django import forms

from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import Profile, CustomUser
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
   
   
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin', 'fullname')
    list_filter = ('is_admin', )

    fieldsets = (
        ('Main', {'fields':('email', 'phone_number', 'fullname', 'password', 'address', 'gender', 'activity')}),
        ('Permissions', {'fields':('is_active', 'is_admin')}),
    )


    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'fullname', 'password1', 'password2', 'address')}),

    )

    search_fields = ('email', 'fullname')
    ordering = ('fullname',)
    filter_horizontal = ()
    inlines = [ProfileInline]

admin.site.unregister(Group)
admin.site.register(CustomUser, UserAdmin)
