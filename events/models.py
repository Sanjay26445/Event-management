from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('organizer', 'Event Organizer'),
        ('attendee', 'Attendee'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def is_organizer(self):
        return self.role == 'organizer'
    
    def is_attendee(self):
        return self.role == 'attendee'


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    max_seats = models.IntegerField(validators=[MinValueValidator(1)])
    available_seats = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['date', 'time']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return self.title
    
    def is_past(self):
        from datetime import datetime
        event_datetime = datetime.combine(self.date, self.time)
        event_datetime_aware = timezone.make_aware(event_datetime)
        return event_datetime_aware < timezone.now()
    
    def is_full(self):
        return self.available_seats <= 0
    
    def get_booked_seats(self):
        return self.max_seats - self.available_seats
    
    def get_revenue(self):
        return Booking.objects.filter(event=self, payment_status='completed').count() * self.price


class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='completed')
    
    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['user', 'event']),
            models.Index(fields=['payment_status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
