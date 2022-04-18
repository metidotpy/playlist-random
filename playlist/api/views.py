# import useful modules
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from ..models import JsonFile, DBFile, Category, Playlist, random_string
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CategorySerializer,
    PlayListAdminSerializer,
    PlayListUserSerializer
)
from rest_framework import serializers
from extensions.db import read_data
import json
import os
import string
import random

#create random string.


# class CategoryListView(views.APIView):    
#     def get(self, request):
#         if request.user.is_superuser or request.user.is_staff:
#             categories = Category.objects.all()
#         else:
#             categories = Category.objects.active()

#         serializer = CategorySerializer(categories, many=True)
        
#         return Response(serializer.data)
    
#     def post(self, request):
#         permission_classes = [IsSuperuserOrAdmin]        
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(views.APIView):
    
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            playlists = category.playlists.active()
        except Category.DoesNotExist:
            return Response({'error': "not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlayListUserSerializer(playlists, many=True)
        return Response(serializer.data)

class PlaylistListView(views.APIView):
    def get(self, request):
        playlists = Playlist.objects.active().all()
        serializer = PlayListUserSerializer(playlists, many=True)
        
        return Response(serializer.data)

class PlaylistDetailView(views.APIView):
    def get(self, request, slug):
        try:
            playlist = Playlist.objects.get(slug=slug, active=True)
        except Playlist.DoesNotExist:
            return Response({"error": 'not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlayListUserSerializer(playlist)
        return Response(serializer.data)

class PlaylistRandomView(views.APIView):
    def get(self, request):
        playlist = random.choice(Playlist.objects.active().all())
        serializer = PlayListUserSerializer(playlist)
        
        return Response(serializer.data)

class LikeView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        try:
            playlist = Playlist.objects.get(slug=slug, active=True)
        except Playlist.DoesNotExist:
            return Response({'error': 'not found.'})
        
        if not request.user in playlist.likes.all():
            playlist.likes.add(request.user)
            playlist.save()
            return Response({'message': 'like added.'})
        else:
            playlist.likes.remove(request.user)
            playlist.save()
            return Response({'message': 'like deleted.'})


class LikesListView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        self.user = request.user
        playlists = Playlist.objects.filter(likes__in=[self.user])

        serializer = PlayListUserSerializer(playlists, many=True)

        return Response(serializer.data)