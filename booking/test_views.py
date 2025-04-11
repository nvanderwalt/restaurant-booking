# test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, time
from booking.models import Table, MenuItem, Booking


class TestViews(TestCase):
    
    def setUp(self):
        # Create test user and admin
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True
        )
        
        # Create a table
        self.table = Table.objects.create(
            table_number=1,
            capacity=4,
            location='WINDOW'
        )
        
        # Create a booking
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            booking_date=tomorrow,
            booking_time=time(19, 0),
            party_size=2,
            status='PENDING'
        )
        
        # Create a menu item
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test description',
            price=10.99,
            category='MAIN'
        )
        
        # Set up test client
        self.client = Client()
    
    def test_home_view(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')
    
    def test_menu_view(self):
        """Test menu page loads with items"""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/menu.html')
        self.assertTrue('mains' in response.context)
    
    def test_booking_view_requires_login(self):
        """Test booking page requires login"""
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Now login and try again
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 200)
    
    def test_my_bookings_view(self):
        """Test my bookings page"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bookings']), 1)
    
    def test_cancel_booking(self):
        """Test booking cancellation"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        
        # Check booking is now cancelled
        updated_booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(updated_booking.status, 'CANCELLED')
    
    def test_admin_dashboard_access(self):
        """Test admin dashboard access"""
        # Regular user cannot access
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Admin can access
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_confirm_booking(self):
        """Test admin confirming booking"""
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(reverse('admin_confirm_booking', args=[self.booking.id]))