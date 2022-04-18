from rest_framework import views
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from extensions.db import read_data
from playlist.models import Playlist, JsonFile, DBFile, Category, random_string
from .permissions import IsSuperuserOrAdmin, IsSuperuser
from .serializers import JsonFileSerializer, DBFileSerializer, CategorySerializer, PlaylistSerializer
import json


class JsonFileView(views.APIView):
    """
    this file read a json file.
    datas to playlist model.
    """
    permission_classes = [IsSuperuserOrAdmin]
    
    def post(self, request):
        slug = random_string().strip()
        repeats = {}
        serializer = JsonFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            category = serializer.data.get('category')
            with open(serializer.data.get('file').replace("/", "\\")[1:], 'r') as f:
                playlists = json.loads(f.read())

            for key, value in playlists.items():
                url = key
                name = value[0]
                creator = value[1]
                creator_link = value[2]
                iframe = value[3]

                if Playlist.objects.filter(url=url, name=name, creator=creator, creator_link=creator_link, iframe=iframe).exists():
                    repeats[url] = [name, creator, creator_link, iframe]
                    continue
                
                if Playlist.objects.filter(slug=slug).exists():
                    slug = random_string().strip()

                playlist = Playlist(url=url, name=name, creator=creator, creator_link=creator_link, iframe=iframe, author=request.user, active=True, slug=slug)
                playlist.save()
                playlist.category.set(category)
            if repeats:
                data = serializer.data
                data['repeat']='this datas already exists.'
                data['datas'] = repeats
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DBFileView(views.APIView):
    permission_classes = [IsSuperuserOrAdmin]
    
    def post(self, request):
        slug = random_string().strip()
        repeats = {}
        serializer = DBFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            category = serializer.data.get('category')
            read_data.connection(file=serializer.data.get('file').replace("/", "\\")[1:])
            playlists = read_data.read_data()
            for key, value in playlists.items():
                url = key
                name = value[0]
                creator = value[1]
                creator_link = value[2]
                iframe = value[3]
                
                if Playlist.objects.filter(url=url, name=name, creator=creator, creator_link=creator_link, iframe=iframe).exists():
                    repeats[url] = [name, creator, creator_link, iframe]
                    continue
    
                if Playlist.objects.filter(slug=slug).exists():
                    slug = random_string().strip()

                playlist = Playlist(url=url, name=name, creator=creator, creator_link=creator_link, iframe=iframe, author=request.user, active=True, slug=slug)
                playlist.save()
                playlist.category.set(category)
            if repeats:
                data=serializer.data
                data['repeat']='this datas already exists.'
                data['datas'] = repeats
                return Response(data, status=status.HTTP_201_CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListAdmin(views.APIView):
    permission_classes = [IsSuperuserOrAdmin]
    
    def get(self, request):
        categories = Category.objects.all()
        
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAdmin(views.APIView):
    permission_classes = [IsSuperuserOrAdmin]
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteSuperuser(views.APIView):
    permission_classes = [IsSuperuser]
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response({'message': 'deleted.'}, status=status.HTTP_204_NO_CONTENT)


class AllPlaylists(views.APIView):
    permission_classes = [IsSuperuserOrAdmin]
    def get(self, request):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)

        if serializer.is_valid():
            playlist = Playlist.objects.create(url = serializer.validated_data['url'], name=serializer.validated_data['name'], creator=serializer.validated_data['creator'], creator_link = serializer.validated_data['creator_link'], iframe=serializer.validated_data['iframe'], author=request.user, active=serializer.validated_data['active'])
            playlist.save()
            playlist.category.set(serializer.validated_data['category'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetail(views.APIView):
    permission_classes  = [IsSuperuserOrAdmin]
    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk = pk)
        except Playlist.DoesNotExist:
            return Response({"error": "not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = PlaylistSerializer(playlist)

        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk = pk)
        except Playlist.DoesNotExist:
            return Response({"error": "not found."}, status.HTTP_404_NOT_FOUND)
        
        serializer = PlaylistSerializer(playlist, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDelete(views.APIView):
    permission_classes = [IsSuperuser]

    def delete(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk = pk)
        except Playlist.DoesNotExist:
            return Response({"error": "not found."}, status.HTTP_404_NOT_FOUND)
        
        playlist.delete()
        return Response({"message": 'deleted'}, status=status.HTTP_204_NO_CONTENT)