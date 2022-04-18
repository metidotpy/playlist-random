"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.api.views import activate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('accounts.api.urls')),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('api/playlist/', include('playlist.api.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/admin/', include('playlist_admin.api.urls')),
]

from django.conf import settings
from django.conf.urls.static import static


urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
