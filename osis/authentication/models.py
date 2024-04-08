# models.py
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):

    def create_user(self, username, name, role, password=None, password2=None):
        if not username:
            raise ValueError("username must have an email addressor phone Number")
        user = self.model(
            username=username,
            name=name,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, role, password=None):
        user = self.create_user(
            username=username,
            name=name,
            role=role,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=255,unique=True)
    
    name = models.CharField(max_length=20)
    role = models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


