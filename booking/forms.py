
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Table, MenuItem

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'party_size', 'notes']
        widgets = {
            'booking_date': DateInput(),
            'booking_time': TimeInput(),
            'party_size': forms.NumberInput(attrs={'min': '1', 'max': '20'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to today
        from datetime import datetime
        self.fields['booking_date'].widget.attrs['min'] = datetime.now().date()
        
    def clean_booking_date(self):
        date = self.cleaned_data.get('booking_date')
        from datetime import datetime
        today = datetime.now().date()
        if date < today:
            raise forms.ValidationError("You cannot book a date in the past")
        return date
    
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'location']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'image', 'vegetarian', 'vegan', 'gluten_free']