from django.db import models
from accounts.models import User
import random, string

def random_string():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

# Create your models here.

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

class PlaylistManager(models.Manager):
    def active(self):
        return self.filter(active=True)
    def inactive(self):
        return self.filter(active=True)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    def __str__(self):
        return self.name

class Playlist(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=150)
    creator = models.CharField(max_length=150)
    creator_link = models.URLField()
    iframe = models.TextField()
    slug = models.SlugField(unique=True, default=random_string().strip(), max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='playlists')
    likes = models.ManyToManyField(User, through="LikePlaylists", related_name='likes', blank=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PlaylistManager()

    def category_to_str(self):
        return ", ".join([category.name for category in self.category.active()])

    def __str__(self):
        return self.name
    
class JsonFile(models.Model):
    file = models.FileField(upload_to='jsons/')
    category = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class DBFile(models.Model):
    file = models.FileField(upload_to='databases/')
    category = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class LikePlaylists(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)