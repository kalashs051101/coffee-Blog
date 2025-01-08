from django.contrib import admin
from BlogApp.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser 

admin.site.register(CustomUser)
# @admin.register(CustomUser)
# class UserAdmin(UserAdmin):
#     list_display=['id','firstname','lastname','username','email','password']


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display=['id','name','description','image','created_at','updated_at','user']

