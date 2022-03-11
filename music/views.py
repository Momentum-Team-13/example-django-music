from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Album, Artist, Genre
from .forms import AlbumForm
from .view_helpers import album_is_favorited, check_admin_user


def home(request):
    if request.user.is_authenticated:
        return redirect("list_albums")
    return render(request, "music/home.html")


@login_required
def list_albums(request):
    sort_by = request.GET.get("sort") or "title"
    albums = Album.objects.order_by(sort_by)
    return render(
        request, "music/list_albums.html", {"albums": albums, "sort_by": sort_by}
    )


@login_required
@user_passes_test(check_admin_user)
def add_album(request):
    if request.method == "POST":
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save()

            return redirect("show_album", pk=album.pk)
    else:
        form = AlbumForm()

    return render(request, "music/add_album.html", {"form": form})


@login_required
def show_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    favorited = album_is_favorited(album, request.user)
    if favorited:
        toggle_favorited_url = "delete_favorite"
    else:
        toggle_favorited_url = "add_favorite"
    return render(
        request,
        "music/show_album.html",
        {
            "album": album,
            "genres": album.genres.all(),
            "favorited": favorited,
            "toggle_favorited_url": toggle_favorited_url,
        },
    )


@login_required
@user_passes_test(check_admin_user)
def edit_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    if request.method == "GET":
        form = AlbumForm(instance=album)
    else:
        form = AlbumForm(data=request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect("list_albums")
        else:
            print(form.errors)

    return render(request, "music/edit_album.html", {"form": form, "album": album})


@login_required
@user_passes_test(check_admin_user)
def delete_album(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == "POST":
        album.delete()
        messages.success(request, "Album deleted.")
        return redirect("list_albums")

    return render(request, "music/delete_album.html", {"album": album})


@login_required
def show_genre(request, slug):
    # albums = Album.objects.filter(genres__slug=slug)
    # I could do this ☝️ but...
    # even better to get all the albums associated with a genre:
    genre = get_object_or_404(Genre, slug=slug)
    albums = genre.albums.all()

    return render(request, "music/show_genre.html", {"genre": genre, "albums": albums})


@login_required
def add_favorite(request, album_pk):
    # when we create a M2M relationship, we need TWO instances
    # here we need the album object AND the user object
    album = get_object_or_404(Album, pk=album_pk)
    user = request.user
    user.favorite_albums.add(album)
    # just redirect to the show_album page
    return redirect("show_album", pk=album.pk)


@login_required
def delete_favorite(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    request.user.favorite_albums.remove(album)

    return redirect("show_album", pk=album.pk)
