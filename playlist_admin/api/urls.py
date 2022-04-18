from django.urls import path
from . import views

urlpatterns = [
    path('json-file/', views.JsonFileView.as_view(), name='json-file'),
    path('db-file/', views.DBFileView.as_view(), name='db-file'),
    path('categories/', views.CategoryListAdmin.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetailAdmin.as_view(), name='category-detail'),
    path('category/delete/<int:pk>/', views.CategoryDeleteSuperuser.as_view(), name='category-delete'),
    path("playlists/", views.AllPlaylists.as_view(), name="playlist-list"),
    path("playlist/<int:pk>/", views.PlaylistDetail.as_view(), name="playlist-detail"),
    path("playlist/delete/<int:pk>/", views.PlaylistDelete.as_view(), name='playlist-delete'),
]
