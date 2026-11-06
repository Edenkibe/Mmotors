from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)
    role_choise= [
            ('communicateur', 'communicateur'),
            ('promoteur', 'promoteur'),
            ('secretaire', 'secretaire'),
        ]
    role=models.CharField(
            max_length=20,
            choices=role_choise,
            blank=True,
            null=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
   
