from django.contrib import admin
from django.urls import path
from BlogApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('',home,name='home'),
    path('Registration/',Registration,name='Registration'),
    path('login_view/',login_view,name='login_view'),
    path('logout_view/',logout_view,name='logout_view'),

    path('update_view/',update_view,name='update_view'),
    path('dashboard/',dashboard,name='dashboard'),
    path('Blog_view/',Blog_view,name='Blog_view'),
    path('Blog_register/',Blog_register,name='Blog_register'),
    path('Blog_delete/',Blog_delete,name='Blog_delete'),
    path('Blog_update/',Blog_update,name='Blog_update'),
    path('individual_show/',individual_show,name='individual_show'),
    path('change_password/',change_password,name='change_password'),

    path('otp/',otp,name='otp'),

    path('verify_email/<token>',verify_email,name='verify_email'),

    path('forgot_password/',forgot_password,name='forgot_password'),
    path('otp_reset_password/',otp_reset_password,name='otp_reset_password'),
    path('reset_password/',reset_password,name='reset_password'),
    path('search_result/',search_result,name='search_result'),

    path('pikachu/',pikachu,name='pikachu'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()