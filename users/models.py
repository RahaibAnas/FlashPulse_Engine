from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

from uuid import uuid4

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email Must Required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        customer = 'CUSTOMER','customer'
        admin = 'ADMIN','admin'

    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=10,choices=RoleChoice.choices,default=RoleChoice.customer)
    username = None
    token_verified= models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
