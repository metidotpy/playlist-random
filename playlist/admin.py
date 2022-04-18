from django.contrib import admin
from .models import JsonFile, DBFile, Category, Playlist

# Register your models here.

admin.site.register(Category)
admin.site.register(JsonFile)
admin.site.register(Playlist)