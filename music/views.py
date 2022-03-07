from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Album, Artist
from .forms import AlbumForm


def list_albums(request):
    albums = Album.objects.all().order_by("title")
    return render(request, "music/list_albums.html", {"albums": albums})


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
        {"album": album},
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
