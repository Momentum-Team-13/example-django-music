from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Album, Artist, Genre
from users.models import CustomUser
from .forms import AlbumForm
from .view_helpers import album_is_favorited, check_admin_user
from django.db.models import Exists, OuterRef, Q


def home(request):
    if request.user.is_authenticated:
        return redirect("list_albums")
    return render(request, "music/home.html")


@login_required
def list_albums(request):
    sort_by = request.GET.get("sort") or "title"
    albums = Album.objects.annotate(
        favorited=Exists(
            CustomUser.objects.filter(
                favorite_albums=OuterRef("pk"), pk=request.user.pk
            )
        )
    ).order_by(sort_by)
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

    return render(
        request,
        "music/show_album.html",
        {
            "album": album,
            "genres": album.genres.all(),
            "favorited": favorited,
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
def favorite(request, album_pk):
    # I have to check the headers (which I set myself in the js!)
    request_is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    # when we create a M2M relationship, we need TWO instances
    # here we need the album object AND the user object
    album = get_object_or_404(Album, pk=album_pk)
    user = request.user
    if request.method == "POST":
        user.favorite_albums.add(album)
        favorited = True
    elif request.method == "DELETE":
        user.favorite_albums.remove(album)
        favorited = False

    if request_is_ajax:
        return JsonResponse({"weDidIt": "YAY", "favorited": favorited})

    return redirect("show_album", pk=album.pk)


@login_required
def delete_favorite(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    request.user.favorite_albums.remove(album)

    return redirect("show_album", pk=album.pk)


def search(request):
    title_search_term = request.GET.get("title")
    artist_search_term = request.GET.get("artist")
    if title_search_term:
        # search the database using the search term from query params
        results = Album.objects.filter(title__icontains=title_search_term).order_by(
            "title"
        )
    elif artist_search_term:
        results = Album.objects.filter(
            artist__name__icontains=artist_search_term
        ).order_by("title")
    else:
        return redirect("list_albums")

    # send back a response with the filter query results
    return render(
        request,
        "music/list_albums.html",
        {"albums": results, "sort_by": "title"},
    )


def search_by_title_and_artist(request):
    """Return results for a search on title AND artist."""
    # ?artist=prince&title=raspberry
    artist_search_term = request.GET.get("artist")
    title_search_term = request.GET.get("title")
    # query the database
    # results have to match BOTH title and artist with this syntax
    results = Album.objects.filter(
        title__icontains=title_search_term, artist__name__icontains=artist_search_term
    )
    # return the results using the list template
    # you don't have to do this! You could render a template that is specifically created for search results.
    return render(request, "music/list_albums.html", {"albums": results})


def search_by_artist_or_title(request):
    """Return results for a search on title OR artist."""
    # this search could work with the existing search form
    query = request.GET.get("q")
    # search using a logical OR operator, the `|` character, and Django's `Q` objects
    # https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects
    # results can match EITHER album title OR artist name
    results = Album.objects.filter(
        Q(title__icontains=query) | Q(artist__name__icontains=query)
    )

    return render(request, "albums/list_albums.html", {"albums": results})
