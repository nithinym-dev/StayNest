from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Room
from datetime import datetime, timedelta
from decimal import Decimal  # Make sure this import is present

User = get_user_model()

class Booking(models.Model):
    BOOKING_TYPES = (
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPES)
    
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    
    # Pricing details
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username}"
    
    @property
    def duration_days(self):
        return (self.check_out_date - self.check_in_date).days
    
    def save(self, *args, **kwargs):
        # Calculate amounts only if they haven't been set manually
        if not self.base_amount or self.base_amount == 0:
            if self.booking_type == 'daily':
                self.base_amount = self.room.daily_rate * Decimal(str(self.duration_days))
            else:
                # Fix: Convert the division result to Decimal
                months = Decimal(str(self.duration_days)) / Decimal('30')
                self.base_amount = self.room.monthly_rate * months
        
        # Calculate total amount
        if not self.total_amount or self.total_amount == 0:
            self.total_amount = self.base_amount + self.security_deposit
        
        super().save(*args, **kwargs)
