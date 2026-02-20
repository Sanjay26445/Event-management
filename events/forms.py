from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone
from .models import CustomUser, Event, Booking


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, initial='attendee')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_image')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control'})


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date', 'time', 'location', 'price', 'max_seats', 'image')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Event Title'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 5, 'placeholder': 'Event Description'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['time'].widget.attrs.update({'class': 'form-control', 'type': 'time'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Event Location'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'})
        self.fields['max_seats'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Maximum Seats'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if date and time:
            from datetime import datetime
            event_datetime = datetime.combine(date, time)
            event_datetime_aware = timezone.make_aware(event_datetime)
            if event_datetime_aware < timezone.now():
                raise forms.ValidationError("Event date and time must be in the future.")
        
        return cleaned_data


class EventSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search events by title...'
        })
    )
    date_filter = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    price_filter = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Prices'),
            ('free', 'Free Events'),
            ('paid', 'Paid Events'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
