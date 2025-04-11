from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from booking.forms import BookingForm, RegisterForm, TableForm, MenuItemForm
from booking.models import Table
from django.contrib.auth.models import User


class TestForms(TestCase):
    
    def setUp(self):
        # Create user for duplicate email testing
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password123'
        )
        
        # Create table for duplicate number testing
        Table.objects.create(
            table_number=1,
            capacity=4,
            location='WINDOW'
        )
    
    def test_booking_form_valid_data(self):
        """Test booking form with valid data"""
        tomorrow = timezone.now().date() + timedelta(days=1)
        form = BookingForm(data={
            'booking_date': tomorrow,
            'booking_time': '19:00:00',
            'party_size': 4,
            'notes': 'Test booking'
        })
        self.assertTrue(form.is_valid())
    
    def test_booking_form_invalid_date(self):
        """Test booking form with past date"""
        yesterday = timezone.now().date() - timedelta(days=1)
        form = BookingForm(data={
            'booking_date': yesterday,
            'booking_time': '19:00:00',
            'party_size': 4
        })
        self.assertFalse(form.is_valid())
        self.assertIn('booking_date', form.errors)
    
    def test_register_form_valid_data(self):
        """Test register form with valid data"""
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        })
        self.assertTrue(form.is_valid())
    
    def test_register_form_duplicate_email(self):
        """Test register form with duplicate email"""
        form = RegisterForm(data={
            'username': 'newuser',
            'email': 'existing@example.com',  # Already exists
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_table_form_valid_data(self):
        """Test table form with valid data"""
        form = TableForm(data={
            'table_number': 2,
            'capacity': 6,
            'location': 'BALCONY'
        })
        self.assertTrue(form.is_valid())
    
    def test_table_form_duplicate_number(self):
        """Test table form with duplicate number"""
        form = TableForm(data={
            'table_number': 1,  # Already exists
            'capacity': 6, 
            'location': 'BALCONY'
        })
        self.assertFalse(form.is_valid())
    
    def test_menu_item_form_valid_data(self):
        """Test menu item form with valid data"""
        form = MenuItemForm(data={
            'name': 'Test Item',
            'description': 'Test description',
            'price': '12.99',
            'category': 'MAIN'
        })
        self.assertTrue(form.is_valid())