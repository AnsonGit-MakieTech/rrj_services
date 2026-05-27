from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class AuthenticatedUser(AbstractUser):
#     # password already exists in AbstractUser
#     # username already exists in AbstractUser
#     # email already exists in AbstractUser
#     full_name = models.CharField(max_length=255 , blank=True, null=True)
#     contact_number = models.CharField(max_length=255 , blank=True, null=True)
#     full_address = models.TextField( blank=True, null=True)
    
    

# class Service(models.Model):
#     name = models.CharField(max_length=255 , blank=True, null=True)
#     description = models.TextField( blank=True, null=True)
#     min_price = models.IntegerField( default=0)
#     max_price = models.IntegerField( default=0)
#     is_active = models.BooleanField( default=True)
#     image = models.ImageField(upload_to='services/', blank=True, null=True)


    
# class BookingRequest(models.Model):
#     owner = models.ForeignKey(AuthenticatedUser, on_delete=models.CASCADE , related_name='booking_requests')
    




