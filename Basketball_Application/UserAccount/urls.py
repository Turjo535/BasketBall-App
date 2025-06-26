
from django.urls import path
from .views import UserRegistrationView, UserLoginView,LogoutView, EmailValidationView,VerifyOTPView,UserChangePasswordView, ForgetPasswordResetView
from rest_framework_simplejwt.views import TokenRefreshView   

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('validate-email/', EmailValidationView.as_view(), name='email-validation'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('forget-password-reset/', ForgetPasswordResetView.as_view(), name='reset-password'),

]