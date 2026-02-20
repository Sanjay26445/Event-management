from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/registrations/', views.event_registrations, name='event_registrations'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    
    # Bookings
    path('events/<int:pk>/register/', views.register_event, name='register_event'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Admin
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/events/', views.manage_events, name='manage_events'),
]
