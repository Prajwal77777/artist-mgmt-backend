from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    class RoleChoices(models.TextChoices):
        SUPER_ADMIN = 'super_admin', _('Super Admin')
        ARTIST_MANAGER = 'artist_manager', _('Artist Manager')
        ARTIST = 'artist', _('Artist')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    role = models.CharField(
        max_length=20, choices=RoleChoices.choices, default=RoleChoices.SUPER_ADMIN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
