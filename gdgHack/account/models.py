from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager that supports user creation with only email, password, and role.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(max_length=100, unique=True,default="email@example.com")
    role = models.CharField(
        max_length=20, 
        choices=[('admin', 'admin'), ('', ''), ('', ''),('','')],  # add user roles here 
        default='admin'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Only email is required for user creation

    # Add unique related_name for groups and permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Unique related_name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    # Override the default related_name for user_permissions to avoid conflicts
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()  # Link to custom manager

    def __str__(self):
        return self.email
# User model
#class User(AbstractUser):
 #   email = models.EmailField(unique=True)
  #password = models.CharField(max_length=128)
   # role = models.CharField(max_length=50)  #patient , technicien , admin 

