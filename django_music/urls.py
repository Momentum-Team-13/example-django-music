"""django_music URL Configuration

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
from django.conf import settings
from django.urls import path
from music import views as music_views

urlpatterns = [
    path("", music_views.list_albums, name="home"),
    path("admin/", admin.site.urls),
    path("albums/", music_views.list_albums, name="list_albums"),
    path("albums/new", music_views.add_album, name="add_album"),
    path("albums/<int:pk>", music_views.show_album, name="show_album"),
    path("albums/<int:pk>/edit", music_views.edit_album, name="edit_album"),
    path("albums/<int:pk>/delete", music_views.delete_album, name="delete_album"),
]

if settings.DEBUG:
    import debug_toolbar
    from django.urls import include

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
