
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login_VF.as_view(), name='login'),
    path('registration', registration_VF.as_view(), name='registration'),
    path('forget_password', forget_password_VF.as_view(), name='forget_password'),
    path('generate_new_password', generate_new_password_VF.as_view(), name='generate_new_password'),
    


    path('templates', templates_VF, name='templates'),
    path('register', register_VF, name='register'),
    path('', install_VF, name='install'),
    path('download/<str:method>', download_VF, name='download'),
    # path('download/window', download_windows_VF, name='download'),
    path('installation_guide', installation_guide_VF, name='installation_guide'),


    path('error_form', error_form, name='error_form'),

    path('new_password', new_password_VF, name='new_password'),
    path('reset_password', reset_password_VF, name='reset_password'),
    
]
