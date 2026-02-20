from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Booking


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'bio', 'profile_image')}),
    )
    list_display = ('username', 'email', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'date', 'time', 'price', 'available_seats', 'created_at')
    list_filter = ('date', 'price', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Details', {
            'fields': ('date', 'time', 'location', 'price')
        }),
        ('Capacity', {
            'fields': ('max_seats', 'available_seats')
        }),
        ('Organizer', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'booking_date', 'payment_status')
    list_filter = ('payment_status', 'booking_date')
    search_fields = ('user__username', 'event__title')
    readonly_fields = ('booking_date',)
