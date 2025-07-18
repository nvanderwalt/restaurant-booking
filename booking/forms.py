
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Table, MenuItem


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class BookingForm(forms.ModelForm):
    TIME_SLOTS = [
        ('12:00:00', '12:00 PM'),
        ('12:30:00', '12:30 PM'),
        ('13:00:00', '1:00 PM'),
        ('13:30:00', '1:30 PM'),
        ('14:00:00', '2:00 PM'),
        ('14:30:00', '2:30 PM'),
        ('17:00:00', '5:00 PM'),
        ('17:30:00', '5:30 PM'),
        ('18:00:00', '6:00 PM'),
        ('18:30:00', '6:30 PM'),
        ('19:00:00', '7:00 PM'),
        ('19:30:00', '7:30 PM'),
        ('20:00:00', '8:00 PM'),
        ('20:30:00', '8:30 PM'),
        ('21:00:00', '9:00 PM'),
    ]

    booking_time = forms.ChoiceField(
        choices=TIME_SLOTS, label="Booking Time"
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'party_size', 'notes']
        widgets = {
            'booking_date': DateInput(),
            'party_size': forms.NumberInput(
                attrs={'min': '1', 'max': '20'}
            ),
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
            raise forms.ValidationError(
                "You cannot book a date in the past"
            )
        return date

    def clean_booking_time(self):
        """Convert time slot string to a proper time object"""
        time_str = self.cleaned_data.get('booking_time')
        from datetime import datetime
        time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
        return time_obj


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.'
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.'
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use."
            )
        return email


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'capacity', 'location']
        widgets = {
            'table_number': forms.NumberInput(attrs={'min': '1'}),
            'capacity': forms.NumberInput(attrs={'min': '1', 'max': '20'}),
        }

    def clean_table_number(self):
        table_number = self.cleaned_data.get('table_number')
        if table_number <= 0:
            raise forms.ValidationError(
                "Table number must be a positive number."
            )
        return table_number

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity <= 0:
            raise forms.ValidationError(
                "Table capacity must be a positive number."
            )
        return capacity


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'name', 'description', 'price', 'category', 'image',
            'vegetarian', 'vegan', 'gluten_free'
        ]
        widgets = {
            'price': forms.NumberInput(
                attrs={'min': '0.01', 'step': '0.01'}
            ),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError(
                "Price must be a positive number."
            )
        return price
