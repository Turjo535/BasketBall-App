
from django.urls import path
from .views import UserRegistrationView, UserLoginView, EmailValidationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('validate-email/', EmailValidationView.as_view(), name='email-validation'),
    
]