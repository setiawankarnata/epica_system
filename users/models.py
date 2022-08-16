from django.db import models
from .validators import empty_value
import uuid
from django.db import models
from django.contrib.auth.models import User
from .validators import empty_value
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.name == "" or self.name is None:
            raise ValidationError(_("Name of department must be filled!"), code="invalid_name")

        if self.description == "" or self.description is None:
            raise ValidationError(_("Description of department must be filled!"), code="invalid_description")

    def __str__(self):
        return self.name


class Profile(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    BOD = [
        ('Y', 'BOD'),
        ('N', 'Non BOD')
    ]
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    profile2user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='user2profile')
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)
    bod = models.CharField(max_length=1, choices=BOD, blank=True, null=True)
    profile2department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def photo_url(self):
        try:
            url = self.photo.url
        except NameError:
            url = ''
        return url
