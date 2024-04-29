from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('loginregister/', views.LoginRegisterView.as_view(), name='loginregister'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile')
]
