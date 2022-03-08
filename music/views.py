from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Album, Artist, Genre
from .forms import AlbumForm


def home(request):
    if request.user.is_authenticated:
        return redirect("list_albums")
    return render(request, "music/home.html")


@login_required
def list_albums(request):
    albums = Album.objects.all().order_by("title")
    return render(request, "music/list_albums.html", {"albums": albums})


@login_required
def add_album(request):
    if request.method == "POST":
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save()

            return redirect("show_album", pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, "music/add_album.html", {"form": form})


def show_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(
        request,
        "music/show_album.html",
        {"album": album, "genres": album.genres.all()},
    )


def edit_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == "GET":
        form = AlbumForm(instance=album)
    else:
        form = AlbumForm(data=request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect("list_albums")

    return render(request, "music/edit_album.html", {"form": form, "album": album})


def delete_album(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        album.delete()
        messages.success(request, "Album deleted.")
        return redirect("list_albums")

    return render(request, "music/delete_album.html", {"album": album})


def show_genre(request, slug):
    # albums = Album.objects.filter(genres__slug=slug)
    # I could do this ☝️ but...
    # even better to get all the albums associated with a genre:
    genre = get_object_or_404(Genre, slug=slug)
    albums = genre.albums.all()

    return render(request, "music/show_genre.html", {"genre": genre, "albums": albums})
