from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['slug', 'username', 'email', 'phone', 'address']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'profile']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'website', 'email', 'address']