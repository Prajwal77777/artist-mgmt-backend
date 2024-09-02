from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):

    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[(
        'super_user', 'Super User'), ('artist_manager', 'Artist Manager'), ('artist', 'Artist')], default='super_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[(
        'male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'


class Artist(models.Model):
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=100, null=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='artists')
    gender = models.CharField(max_length=10, choices=[(
        'male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male')
    first_year_release = models.IntegerField(default=2000)
    no_of_albums_released = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'


class Music(models.Model):
    title = models.CharField(max_length=100, null=True)
    album_name = models.CharField(max_length=100, null=True)
    duration = models.DurationField()
    genre = models.CharField(max_length=50, choices=[(
        'rnb', 'RNB'), ('country', 'Country'), ('classic', 'Classic'), ('jazz', 'Jazz'), ('rock', 'Rock')])
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='music')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

    class Meta:
        db_table = 'musics'
