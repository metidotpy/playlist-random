from django.urls import path
from . import views

urlpatterns = [
    # path('category/', views.CategoryListView.as_view(), name='category'),
    path('likes/', views.LikesListView.as_view(), name='likes'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category-detail'),
    path('', views.PlaylistListView.as_view(), name="playlist-list"),
    path('<slug:slug>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('pl/random/', views.PlaylistRandomView.as_view(), name='playlist-random'),
    path('like/<slug:slug>/', views.LikeView.as_view(), name='like-post'),
]
