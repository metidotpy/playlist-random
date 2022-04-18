from rest_framework import serializers
from playlist.models import JsonFile, DBFile, Category, Playlist


class JsonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonFile
        fields = '__all__'

class DBFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBFile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Playlist
        fields = [
            'url',
            'name',
            'creator',
            'creator_link',
            'iframe', 
            'slug',
            'author',
            'category',
            'category_to_str',
            'likes',
            'active',
            'created',
            'updated',
        ]