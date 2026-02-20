from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
from .models import CustomUser, Event, Booking
from .forms import CustomUserCreationForm, CustomUserChangeForm, EventForm, EventSearchForm, BookingForm


def home(request):
    """Home page with featured events"""
    featured_events = Event.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'time')[:6]
    
    context = {
        'featured_events': featured_events,
        'total_events': Event.objects.count(),
        'total_users': CustomUser.objects.count(),
    }
    return render(request, 'events/home.html', context)


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'events/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'events/login.html')


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    
    if user.role == 'organizer':
        events = Event.objects.filter(created_by=user)
        total_registrations = Booking.objects.filter(event__created_by=user).count()
        total_revenue = sum(event.get_revenue() for event in events)
        
        context = {
            'events': events,
            'total_registrations': total_registrations,
            'total_revenue': total_revenue,
            'role': 'organizer',
        }
    elif user.role == 'admin':
        total_users = CustomUser.objects.count()
        total_events = Event.objects.count()
        total_bookings = Booking.objects.count()
        recent_bookings = Booking.objects.select_related('user', 'event').order_by('-booking_date')[:10]
        
        context = {
            'total_users': total_users,
            'total_events': total_events,
            'total_bookings': total_bookings,
            'recent_bookings': recent_bookings,
            'role': 'admin',
        }
    else:  # attendee
        bookings = Booking.objects.filter(user=user).select_related('event').order_by('-booking_date')
        
        context = {
            'bookings': bookings,
            'role': 'attendee',
        }
    
    return render(request, 'events/dashboard.html', context)


@login_required
def profile(request):
    """User profile"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'events/profile.html', {'form': form})


def event_list(request):
    """List all events with search and filter"""
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date', 'time')
    form = EventSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        date_filter = form.cleaned_data.get('date_filter')
        price_filter = form.cleaned_data.get('price_filter')
        
        if search:
            events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))
        
        if date_filter:
            events = events.filter(date=date_filter)
        
        if price_filter == 'free':
            events = events.filter(price=0)
        elif price_filter == 'paid':
            events = events.filter(price__gt=0)
    
    context = {
        'events': events,
        'form': form,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """Event detail page"""
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    booking = None
    
    if request.user.is_authenticated:
        booking = Booking.objects.filter(user=request.user, event=event).first()
        is_registered = booking is not None
    
    context = {
        'event': event,
        'is_registered': is_registered,
        'booking': booking,
        'organizer': event.created_by,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def create_event(request):
    """Create new event (organizers only)"""
    if request.user.role != 'organizer':
        messages.error(request, 'Only organizers can create events.')
        return redirect('home')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.available_seats = event.max_seats
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def edit_event(request, pk):
    """Edit event (organizers only)"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.created_by and request.user.role != 'admin':
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, pk):
    """Delete event (organizers only)"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.created_by and request.user.role != 'admin':
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'events/delete_event.html', {'event': event})


@login_required
@require_http_methods(["POST"])
def register_event(request, pk):
    """Register for an event"""
    event = get_object_or_404(Event, pk=pk)
    
    # Check if event is full
    if event.is_full():
        messages.error(request, 'This event is full.')
        return redirect('event_detail', pk=pk)
    
    # Check if already registered
    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('event_detail', pk=pk)
    
    # Create booking
    booking = Booking.objects.create(user=request.user, event=event)
    event.available_seats -= 1
    event.save()
    
    messages.success(request, 'Successfully registered for the event!')
    return redirect('event_detail', pk=pk)


@login_required
@require_http_methods(["POST"])
def cancel_booking(request, booking_id):
    """Cancel event booking"""
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if booking.user != request.user and request.user.role != 'admin':
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('dashboard')
    
    event = booking.event
    booking.delete()
    event.available_seats += 1
    event.save()
    
    messages.success(request, 'Booking cancelled successfully!')
    return redirect('dashboard')


@login_required
def manage_users(request):
    """Manage users (admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    users = CustomUser.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
    }
    return render(request, 'events/manage_users.html', context)


@login_required
def manage_events(request):
    """Manage events (admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    events = Event.objects.all().order_by('-created_at')
    
    context = {
        'events': events,
    }
    return render(request, 'events/manage_events.html', context)


@login_required
def event_registrations(request, pk):
    """View attendee registrations for an event (organizer only)"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.created_by and request.user.role != 'admin':
        messages.error(request, 'You do not have permission to view registrations for this event.')
        return redirect('event_detail', pk=pk)
    
    registrations = Booking.objects.filter(event=event).select_related('user').order_by('-booking_date')
    
    context = {
        'event': event,
        'registrations': registrations,
        'total_registrations': registrations.count(),
    }
    return render(request, 'events/event_registrations.html', context)
