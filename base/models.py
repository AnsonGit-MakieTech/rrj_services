# from django.db import models
# from django.contrib.auth.models import AbstractUser

# # Create your models here.
# # bandoquillosarim@gmail.com
# # Password@123
# # https://nifty-build-fix-pro.base44.app

# class AuthenticatedUser(AbstractUser):
#     # password already exists in AbstractUser
#     # username already exists in AbstractUser
#     # email already exists in AbstractUser
#     full_name = models.CharField(max_length=255 , blank=True, null=True)
#     contact_number = models.CharField(max_length=255 , blank=True, null=True)
#     full_address = models.TextField( blank=True, null=True)

#     def __str__(self):
#         return f"{self.pk} - {self.full_name}"

# class SystemSettings(models.Model):
#     tagline = models.CharField(max_length=255 , blank=True, null=True)
#     description = models.TextField( blank=True, null=True)
    
#     def __str__(self):
#         return f"{self.pk} - {self.tagline}"

# class Service(models.Model):
#     name = models.CharField(max_length=255 , blank=True, null=True)
#     description = models.TextField( blank=True, null=True)
#     min_price = models.IntegerField( default=0)
#     max_price = models.IntegerField( default=0)
#     is_active = models.BooleanField( default=True)
#     image = models.ImageField(upload_to='services/', blank=True, null=True)
#     status = models.CharField(
#         max_length=255, choices=( 
#             ('available' , 'Available'),
#             ('unavailable' , 'Unavailable'),
#             ('fully_booked' , 'Fully Booked'),
#         ), 
#         default='available'
#     )

#     def __str__(self):
#         return f"{self.pk} - {self.name}"


    
# class BookingRequest(models.Model):
#     # System Information
#     owner = models.ForeignKey(AuthenticatedUser, on_delete=models.CASCADE , related_name='booking_requests')
#     progress = models.CharField(
#         max_length=255, choices=( 
#             ('pending_quotation' , 'Pending Quotation'),
#             ('quotation_sent' , 'Quotation Sent'),
#             ('waiting_for_payment' , 'Waiting for Payment'),
#             ('payment_verification' , 'Payment Verification'),
#             ('booking_confirmed' , 'Booking Confirmed'),
#             ('scheduled' , 'Scheduled'),
#             ('in_progress' , 'In Progress'),
#             ('completed' , 'Completed'),
#         ), 
#         default='pending_quotation'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     reference_number = models.CharField(max_length=255 , blank=True, null=True)


#     # Customer Information
#     full_name = models.CharField(max_length=255 , blank=True, null=True)
#     email = models.CharField(max_length=255 , blank=True, null=True)
#     contact_number = models.CharField(max_length=255 , blank=True, null=True)
#     full_address = models.TextField( blank=True, null=True)

#     # Service Information
#     service = models.ForeignKey(Service, on_delete=models.CASCADE , related_name='booking_requests')
#     urgency_level = models.CharField(
#         max_length=255, choices=( 
#             ('low' , 'Low'),
#             ('medium' , 'Medium'),
#             ('high' , 'High'),
#             ('emergency' , 'Emergency'),
#         ), 
#         default='low'
#     )
#     preferred_date = models.DateField( blank=True, null=True)
#     square_meters = models.FloatField( default=0.0) # Square Meters (SQM)
#     project_location = models.TextField( blank=True, null=True)
#     service_description = models.TextField( blank=True, null=True)
#     problem_description = models.TextField( blank=True, null=True)

#     # Quotation Information
#     material_cost = models.FloatField( default=0.0)
#     labor_cost = models.FloatField( default=0.0)
#     total_cost = models.FloatField( default=0.0)
#     transaction_notes = models.TextField( blank=True, null=True)

#     # Payment Information
#     amount_paid = models.FloatField( default=0.0)
#     payment_method = models.CharField(
#         max_length=255 , choices=( 
#             ('g-cash' , 'G-Cash'),
#             ('bank-transfer' , 'Bank Transfer'),
#             ('maya' , 'Maya'),
#         ),
#         default='g-cash'
#     )
#     reference_number = models.CharField(max_length=255 , blank=True, null=True)
#     receipt_screenshot = models.ImageField(upload_to='receipts/', blank=True, null=True)
#     approved_payment = models.BooleanField( default=False)

#     def __str__(self):
#         return f"{self.pk} - {self.full_name}"


# class BookingAttachment(models.Model):
#     booking_request = models.ForeignKey(BookingRequest, on_delete=models.CASCADE , related_name='attachments')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # Attachment Information
#     file = models.FileField(upload_to='attachments/', blank=True, null=True)


#     def __str__(self):
#         return f"{self.pk} - {self.file.name}"




# class ChatMessage(models.Model):
#     booking_request = models.ForeignKey(BookingRequest, on_delete=models.CASCADE , related_name='chat_messages')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # Chat Message Information
#     message = models.TextField( blank=True, null=True)
#     sender = models.ForeignKey(AuthenticatedUser, on_delete=models.CASCADE , related_name='chat_messages')
#     receiver = models.ForeignKey(AuthenticatedUser, on_delete=models.CASCADE , related_name='chat_messages')

#     def __str__(self):
#         return f"{self.pk} - {self.message}"
