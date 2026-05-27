from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# bandoquillosarim@gmail.com
# Password@123

class AuthenticatedUser(AbstractUser):
    # password already exists in AbstractUser
    # username already exists in AbstractUser
    # email already exists in AbstractUser
    full_name = models.CharField(max_length=255 , blank=True, null=True)
    contact_number = models.CharField(max_length=255 , blank=True, null=True)
    full_address = models.TextField( blank=True, null=True)

    def __str__(self):
        return f"{self.pk} - {self.full_name}"

class SystemSettings(models.Model):
    tagline = models.CharField(max_length=255 , blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    
    def __str__(self):
        return f"{self.pk} - {self.tagline}"

class Service(models.Model):
    name = models.CharField(max_length=255 , blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    min_price = models.IntegerField( default=0)
    max_price = models.IntegerField( default=0)
    is_active = models.BooleanField( default=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    status = models.CharField(
        max_length=255, choices=( 
            ('available' , 'Available'),
            ('unavailable' , 'Unavailable'),
            ('fully_booked' , 'Fully Booked'),
        ), 
        default='available'
    )

    def __str__(self):
        return f"{self.pk} - {self.name}"


    
class BookingRequest(models.Model):
    owner = models.ForeignKey(AuthenticatedUser, on_delete=models.CASCADE , related_name='booking_requests')
    progress = models.CharField(
        max_length=255, choices=( 
            
        ), 
        default='p'
    )
    """
        Pending Quotation
        Quotation Sent
        Waiting for Payment
        Payment Verification
        Booking Confirmed
        Scheduled
        In Progress
        Completed
    """




