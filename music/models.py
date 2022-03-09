from django.db import models
from django.utils.text import slugify
from users.models import CustomUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Album(BaseModel):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        "Artist", on_delete=models.SET_NULL, null=True, blank=True
    )
    release_date = models.DateField(blank=True, null=True)
    genres = models.ManyToManyField("Genre", related_name="albums")
    favorited_by = models.ManyToManyField(CustomUser, related_name="favorite_albums")

    def __repr__(self):
        return f"<Album {self.title} pk={self.pk} >"

    def __str__(self):
        return self.title


class Artist(BaseModel):
    INDIVIDUAL = "IND"
    GROUP = "GRP"

    ARTIST_TYPE_CHOICES = ((INDIVIDUAL, "individual"), (GROUP, "group"))

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices=ARTIST_TYPE_CHOICES)

    def __repr__(self):
        return f"<Artist {self.name} pk={self.pk}>"

    def __str__(self):
        return self.name


class Genre(BaseModel):
    name = models.CharField(max_length=75)
    slug = models.SlugField(max_length=75, blank=True, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Genre name={self.name}>"

    def save(self):
        self.slug = slugify(self.name)
        super().save()
