from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model


# Create User Model and manager for more customization and control over user authentication

class CustomUserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,phone_number,password=None,is_transporter=False,is_producer=False,country="Togo",city="Lome"):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            country=country,
            city=city,
            is_transporter = False,
            is_producer = False
        )

        user.set_password(password)
        user.save()
        return user



    def create_superuser(self,email,first_name,last_name,phone_number,password=None,is_transporter=True,is_producer=True,country="Togo",city="Lome"):
        email=self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            country=country,
            city=city,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_transporter = True
        user.is_producer = True
        user.set_password(password)
        user.save()
        return user


# The Custom User Model

class TracaoUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    country = CountryField(blank_label='(Sélectionnez un pays)',default="Togo")
    city = models.CharField(max_length=100,default="Lome")

    is_transporter = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    objects = CustomUserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number','country','city']
    
    
    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
    







User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    id_picture = models.ImageField(upload_to='id_pictures', blank=True, null=True)
    
    
    def __str__(self):
        return self.user.email