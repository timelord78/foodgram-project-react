from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username

    def get_username(self):
        return self.email
