from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self,
                    username,
                    firstname,
                    lastname,
                    password,
                    phonenumber,
                    is_staff=False,
                    is_active=True,
                    is_admin=False):
        """
        Create and save a User with the given email and passwords.
        """
        if not email:
            raise ValueError(_('The Username must be set'))
        username = self.normalize_email(username)
        user = self.model(username=username,
                          firstname=firstname,
                          lastname=lastname,
                          password=password,
                          phonenumber=phonenumber)
        phonenumber = phonenumber
        firstname = firstname
        lastname = lastname
        user.set_password(password)
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, firstname, lastname,
                         phonenumber):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(username,
                                password=password,
                                firstname=firstname,
                                lastname=lastname,
                                phonenumber=phonenumber)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
