from django import forms
from .models import Hotel, Room, Booking, Payment, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'capacity', 'price_per_night', 'is_available']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):


    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']