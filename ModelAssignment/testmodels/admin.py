from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['slug', 'username', 'email', 'phone', 'address']
    prepopulated_fields={'slug':    ('username',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'profile']
    prepopulated_fields = {'slug' : ('name',),}


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'website', 'email', 'address']
    prepopulated_fields = {'slug' : ('name',),}

@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    list_display = ['slug', 'author', 'title', 'publisher', 'date_of_pub', 'is_deleted', 'genre']
    prepopulated_fields = {'slug' : ('title','publisher'),}

@admin.register(Collection)
class AdminCollection(admin.ModelAdmin):
    list_display = ['slug', 'name', 'get_books']
    prepopulated_fields = {'slug' : ('name',),}
