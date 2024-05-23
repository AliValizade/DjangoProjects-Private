from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('loginregister/', views.LoginRegisterView.as_view(), name='loginregister'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('verify/', views.VerifyOtpCode.as_view(), name='verify'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserConfirmPasswordResetView.as_view(), name='confirm_reset'),
    path('reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='reset_complete'),
    ]
