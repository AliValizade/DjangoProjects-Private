from django.urls import path, include
from ..views import user_views


app_name = 'accuonts_user'

urlpatterns = [
    path('register/', user_views.UserRegisterView.as_view(), name='register/'),
    path('api/token/login/email', user_views.ObtainTokenByEmail.as_view(), name='email_token'),
    path('api/token/login/phone', user_views.ObtainTokenByPhoneNumber.as_view(), name='phone_token'),
    path('api/logout/', user_views.UserLogoutView.as_view(), name='logout'),
    path('api/token/verify/', user_views.VerifyOtpCodeView.as_view(), name='verify'),
    path('api/token/loginverify', user_views.LoginVerifyOtpCode.as_view(), name='login_verify'),
    path('profile/', user_views.UserProfileView.as_view(), name = 'user_profile'),
    ]

