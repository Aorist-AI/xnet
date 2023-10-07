from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class Packages(models.Model):
    bundle = models.CharField(max_length=20)
    bundle_price = models.IntegerField()
    bundle_length = models.CharField(max_length=10)
    bundle_speed = models.CharField(max_length=15)


class CustomUser(AbstractBaseUser):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=60, unique=True, default="Truth")
    phonenumber = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'phonenumber']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class SelectedPackages(models.Model):
    username = models.CharField(max_length=50)
    bundle = models.CharField(max_length=10)
    speed = models.CharField(max_length=10)
    Expiry = models.CharField(max_length=50)
    balance = models.CharField(max_length=100)
    access_period = models.CharField(max_length=10)
    bundle_id = models.IntegerField()


class Radcheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        managed = False
        db_table = 'radcheck'
