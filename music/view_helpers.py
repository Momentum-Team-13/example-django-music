def album_is_favorited(album, user):
    # how can I tell if a related object exists in the database in django?
    return user.favorite_albums.filter(pk=album.pk).exists()


def check_admin_user(user):
    return user.is_staff
