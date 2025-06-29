from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,name, email,phone,  role, password=None):
        """
        Creates and saves a User with the given email, name, role and password.
        """
        if not name:
            raise ValueError("Users must have a Username")
        if not email:
            raise ValueError("Users must have an email address")
        if not phone:
            raise ValueError("Users must have a phone number")
      

        email = self.normalize_email(email)
        user = self.model(name=name,email=email, phone=phone, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name, email,  phone, role='coach', password=None):
        """
        Creates and saves a superuser.
        We default superusers to 'coach' role, but you can choose any.
        """

        user = self.create_user(name, email,  phone, role, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
 

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('coach',  'Coach'),
    ]
    name       = models.CharField(max_length=255, unique=True)
    email      = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    phone      = models.CharField(max_length=20)
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active  = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    otp_send_time = models.DateTimeField(blank=True, null=True)
    is_admin   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD  = 'name'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

