# test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, time
from decimal import Decimal
from booking.models import Table, MenuItem, Booking
import json


class TestHomeView(TestCase):
    
    def test_home_view(self):
        """Test the home page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/home.html')


class TestMenuView(TestCase):
    
    def setUp(self):
        # Create menu items test
        MenuItem.objects.create(
            name='Test Starter',
            description='Test description',
            price=Decimal('9.99'),
            category='STARTER'
        )
        MenuItem.objects.create(
            name='Test Main',
            description='Test description',
            price=Decimal('19.99'),
            category='MAIN'
        )
        MenuItem.objects.create(
            name='Test Dessert',
            description='Test description',
            price=Decimal('7.99'),
            category='DESSERT'
        )
        MenuItem.objects.create(
            name='Test Drink',
            description='Test description',
            price=Decimal('4.99'),
            category='DRINK'
        )
    
    def test_menu_view(self):
        """Test the menu page loads correctly with items"""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/menu.html')
        
        # Check all menu categories
        self.assertTrue('starters' in response.context)
        self.assertTrue('mains' in response.context)
        self.assertTrue('desserts' in response.context)
        self.assertTrue('drinks' in response.context)
        
        # Check items are displayed
        self.assertEqual(len(response.context['starters']), 1)
        self.assertEqual(len(response.context['mains']), 1)
        self.assertEqual(len(response.context['desserts']), 1)
        self.assertEqual(len(response.context['drinks']), 1)


class TestBookingViews(TestCase):
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create tables
        self.table = Table.objects.create(
            table_number=1,
            capacity=4,
            location='WINDOW'
        )
        Table.objects.create(
            table_number=2,
            capacity=2,
            location='INSIDE'
        )
        
        # Create test booking
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            booking_date=tomorrow,
            booking_time=time(19, 0),
            party_size=2,
            status='CONFIRMED'
        )
        
       
        self.client = Client()
    
    def test_make_booking_view_get(self):
        """Test booking page loads when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking.html')
    
    def test_make_booking_view_unauthorized(self):
        """Test booking page redirects when not logged in"""
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    def test_my_bookings_view(self):
        """Test my bookings page loads correctly"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/my_bookings.html')
        
        # Check if booking is in context
        self.assertEqual(len(response.context['bookings']), 1)
        self.assertEqual(response.context['bookings'][0].id, self.booking.id)
    
    def test_cancel_booking(self):
        """Test cancelling a booking"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        
        # Should redirect to my_bookings page
        self.assertRedirects(response, reverse('my_bookings'))
        
        # Check if booking status is now CANCELLED
        booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(booking.status, 'CANCELLED')
    
    def test_check_availability(self):
        """Test the availability checking endpoint"""
        self.client.login(username='testuser', password='testpassword123')
        
        # Future date for testing
        test_date = (timezone.now().date() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        response = self.client.post(
            reverse('check_availability'),
            {
                'booking_date': test_date,
                'booking_time': '18:00:00',
                'party_size': 2
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Check if response contains available tables
        data = json.loads(response.content)
        self.assertTrue('available_tables' in data)
        self.assertEqual(len(data['available_tables']), 2)  # Both tables should be available


class TestRegistrationView(TestCase):
    
    def test_register_view_get(self):
        """Test register page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'complex_password123',
                'password2': 'complex_password123'
            }
        )
        
        # Should redirect to login page
        self.assertRedirects(response, reverse('login'))
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())


class TestAdminViews(TestCase):
    
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='regularpassword123'
        )
        
        # Create table
        self.table = Table.objects.create(
            table_number=1,
            capacity=4,
            location='WINDOW'
        )
        
        # Create booking
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.booking = Booking.objects.create(
            user=self.regular_user,
            table=self.table,
            booking_date=tomorrow,
            booking_time=time(19, 0),
            party_size=2,
            status='PENDING'
        )
        
        # Create test client
        self.client = Client()
    
    def test_admin_dashboard_access(self):
        """Test admin dashboard access for staff"""
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/dashboard.html')
    
    def test_admin_dashboard_unauthorized(self):
        """Test admin dashboard access is denied for non-staff"""
        self.client.login(username='regularuser', password='regularpassword123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_admin_confirm_booking(self):
        """Test admin can confirm a booking"""
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(reverse('admin_confirm_booking', args=[self.booking.id]))
        
        # Should redirect to admin dashboard
        self.assertRedirects(response, reverse('admin_dashboard'))
        
        # Check if booking status is now CONFIRMED
        booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(booking.status, 'CONFIRMED')
    
    def test_admin_cancel_booking(self):
        """Test admin can cancel a booking"""
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(reverse('admin_cancel_booking', args=[self.booking.id]))
        
        # Should redirect to admin dashboard
        self.assertRedirects(response, reverse('admin_dashboard'))
        
        # Check if booking status is now CANCELLED
        booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(booking.status, 'CANCELLED')


class TestTableManagement(TestCase):
    
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True
        )
        
        # Create table
        self.table = Table.objects.create(
            table_number=1,
            capacity=4,
            location='WINDOW'
        )
        
        # Create test client
        self.client = Client()
        self.client.login(username='adminuser', password='adminpassword123')
    
    def test_table_management_view(self):
        """Test table management page loads correctly"""
        response = self.client.get(reverse('table_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/table_management.html')
        
        # Check table is in context
        self.assertEqual(len(response.context['tables']), 1)
    
    def test_add_table_view(self):
        """Test adding a new table"""
        response = self.client.post(
            reverse('add_table'),
            {
                'table_number': 2,
                'capacity': 6,
                'location': 'BALCONY'
            }
        )
        
        # Should redirect to table management
        self.assertRedirects(response, reverse('table_management'))
        
        # Check if table was created
        self.assertTrue(Table.objects.filter(table_number=2).exists())
    
    def test_edit_table_view(self):
        """Test editing an existing table"""
        response = self.client.post(
            reverse('edit_table', args=[self.table.id]),
            {
                'table_number': 1,
                'capacity': 8,  # Changed capacity
                'location': 'WINDOW'
            }
        )
        
        # Should redirect to table management
        self.assertRedirects(response, reverse('table_management'))
        
        # Check if table was updated
        updated_table = Table.objects.get(id=self.table.id)
        self.assertEqual(updated_table.capacity, 8)
    
    def test_delete_table(self):
        """Test deleting a table"""
        response = self.client.post(reverse('delete_table', args=[self.table.id]))
        
        # Should redirect to table management
        self.assertRedirects(response, reverse('table_management'))
        
        # Check if table was deleted
        self.assertFalse(Table.objects.filter(id=self.table.id).exists())


class TestMenuManagement(TestCase):
    
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True
        )
        
        # Create menu item
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test description',
            price=Decimal('12.99'),
            category='MAIN'
        )
        
        # Create test client
        self.client = Client()
        self.client.login(username='adminuser', password='adminpassword123')
    
    def test_menu_management_view(self):
        """Test menu management page loads correctly"""
        response = self.client.get(reverse('menu_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/menu_management.html')
        
        # Check menu item is in context
        self.assertEqual(len(response.context['mains']), 1)
    
    def test_add_menu_item_view(self):
        """Test adding a new menu item"""
        response = self.client.post(
            reverse('add_menu_item'),
            {
                'name': 'New Item',
                'description': 'New description',
                'price': '15.99',
                'category': 'STARTER',
                'vegetarian': True,
                'vegan': False,
                'gluten_free': True
            }
        )
        
        # Should redirect to menu management
        self.assertRedirects(response, reverse('menu_management'))
        
        # Check if menu item was created
        self.assertTrue(MenuItem.objects.filter(name='New Item').exists())
    
    def test_edit_menu_item_view(self):
        """Test editing an existing menu item"""
        response = self.client.post(
            reverse('edit_menu_item', args=[self.menu_item.id]),
            {
                'name': 'Updated Item',
                'description': 'Updated description',
                'price': '14.99',
                'category': 'MAIN',
                'vegetarian': True,
                'vegan': False,
                'gluten_free': False
            }
        )
        
        # Should redirect to menu management
        self.assertRedirects(response, reverse('menu_management'))
        
        # Check if menu item was updated
        updated_item = MenuItem.objects.get(id=self.menu_item.id)
        self.assertEqual(updated_item.name, 'Updated Item')
        self.assertEqual(updated_item.price, Decimal('14.99'))
    
    def test_delete_menu_item(self):
        """Test deleting a menu item"""
        response = self.client.post(reverse('delete_menu_item', args=[self.menu_item.id]))
        
        # Should redirect to menu management
        self.assertRedirects(response, reverse('menu_management'))
        
        # Check if menu item was deleted
        self.assertFalse(MenuItem.objects.filter(id=self.menu_item.id).exists())