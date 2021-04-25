from django.urls import path
from .views import *

# a decorator to prevent cross site scripting checking
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register',RegisterView.as_view(),name ='register'),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate-email'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name ='activate'),
    path('login',LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('request_reset_link',ResetPasswordView.as_view(), name='request_reset_link'),
    path('reset_user_password/<uidb64>/<token>',CompletePasswordReset.as_view(), name = 'reset_user_password')
] 