from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib.auth.models import BaseUserManager



# Create User Model and manager for more customization and control over user authentication

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        extra_fields.setdefault('is_transporter', False)
        extra_fields.setdefault('is_producer', False)
        extra_fields.setdefault('is_cooperative_source', False)
        extra_fields.setdefault('is_cooperative_destination', False)
        extra_fields.setdefault('country', 'Togo')
        extra_fields.setdefault('city', 'Lome')

        user = self.model(
            email=email,
           **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self,email,password=None,**extra_fields):

        email=self.normalize_email(email)
        
        
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True) 

        extra_fields.setdefault('is_transporter', True)
        extra_fields.setdefault('is_producer', True)
        extra_fields.setdefault('is_cooperative_source', True)
        extra_fields.setdefault('is_cooperative_destination', True)

        return self.create_user(email, password, **extra_fields)


# The Custom User Model

class TracaoUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    cooperative_name = models.CharField(max_length=200,blank=True,null=True)
    first_name = models.CharField(max_length=200,blank=True,null=True)
    last_name = models.CharField(max_length=200,blank=True,null=True)
    phone_number = PhoneNumberField(blank=True,null=True)
    country = CountryField(blank_label='(Sélectionnez un pays)',default="Togo",blank=True,null=True)
    city = models.CharField(max_length=100,default="Lome",blank=True,null=True)

    is_transporter = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    is_cooperative_source = models.BooleanField(default=False)
    is_cooperative_destination = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    objects = CustomUserManager()
    
    
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name','last_name','phone_number','country','city']
    
    
    def __str__(self):
        return self.email

    




# User profil picture




class ProfilePic(models.Model):
    user = models.OneToOneField(TracaoUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    id_picture = models.ImageField(upload_to='id_pictures', blank=True, null=True)
    
    
    def __str__(self):
        return self.user.email


# Stock Management 


# Producteur

class StockProducer(models.Model):
    producer = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_producer': True}, related_name='producer_stocks')
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_source': True}, related_name='cooperative_source_stocks')
    weight = models.FloatField(blank=True, null=True)
    date = models.DateField()

    TYPE_CHOICES = [
        ('cacao', 'Cacao'),
        ('cafe', 'Cafe'),
    ]

    product_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    species = models.TextField(blank=True, null=True)
    origin = models.CharField(max_length=200)
    surface_size = models.FloatField() # in hectares
    production_size = models.FloatField() # in Kg
    
    def __str__(self):
        return f"{self.producer.first_name} { self.producer.last_name} from {self.cooperative.cooperative_name}"
    

# coopérative d'origine

class StockOrigin(models.Model):
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_source': True}, related_name='origin_stocks')
    producer_stock = models.ForeignKey(StockProducer, on_delete=models.CASCADE, related_name='origin_records')
    
    
    def __str__(self):
        return f"{self.producer_stock.producer.first_name} { self.producer_stock.producer.last_name} from {self.cooperative.cooperative_name} with {self.producer_stock.weight}kg of {self.producer_stock.product_type}"


# Acheteur

class StockTransporter(models.Model):
    transporter = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_transporter': True}, related_name='transported_stocks')
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_destination': True}, related_name='cooperative_destination_transports')
    stock_origin = models.ForeignKey(StockOrigin, on_delete=models.CASCADE, related_name='transporter_records')

    def __str__(self):
        return f"{self.transporter.first_name} { self.transporter.last_name} from {self.cooperative.cooperative_name}"


# Coopérative d'arrivage

class StockDestination(models.Model):
    cooperative = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_cooperative_destination': True}, related_name='cooperative_destination_stocks')
    transporter = models.ForeignKey(TracaoUser, on_delete=models.CASCADE, limit_choices_to={'is_transporter': True}, related_name='delivered_stocks')
    stock_origin = models.ForeignKey(StockOrigin, on_delete=models.CASCADE, related_name='destination_records')

    def __str__(self):
        return f"{self.transporter.first_name} { self.transporter.last_name} to {self.cooperative.cooperative_name}"