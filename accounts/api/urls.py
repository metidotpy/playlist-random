from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from . import signals

urlpatterns = [
    path("login/", views.TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    # path('password-reset/', views.RequestPasswordResetEmail.as_view(), name='password-reset'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace="password_reset")),
    path('profile/', views.Profile.as_view(), name='profile'),

]
