from .models import Album, Artist
from django import forms


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("title", "artist", "release_date", "genres")
