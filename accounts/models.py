from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('user', 'User'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    phone_number = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Assign user to appropriate group
        if self.user_type == 'admin':
            group, created = Group.objects.get_or_create(name='Admin')
        elif self.user_type == 'owner':
            group, created = Group.objects.get_or_create(name='Owner')
        else:
            group, created = Group.objects.get_or_create(name='User')
        self.groups.add(group)

class OwnerProfile(models.Model):
    DOCUMENT_TYPES = (
        ('pan', 'PAN Card'),
        ('aadhaar', 'Aadhaar Card'),
        ('business_id', 'Business ID'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50)
    document_image = models.ImageField(upload_to='property_images/')
    business_name = models.CharField(max_length=100)
    business_address = models.TextField()
    verification_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Save the profile first
        super().save(*args, **kwargs)
        
        # Update user verification status based on profile status
        if self.verification_status == 'approved' and not self.user.is_verified:
            self.user.is_verified = True
            self.user.save()
        elif self.verification_status != 'approved' and self.user.is_verified:
            self.user.is_verified = False
            self.user.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.business_name}"
