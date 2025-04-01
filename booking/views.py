
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count
from .models import Booking, Table, MenuItem
from .forms import BookingForm, RegisterForm, TableForm, MenuItemForm
from datetime import datetime


def home(request):
    """Homepage view"""
    return render(request, 'booking/home.html')

def menu(request):
    """Menu view"""
    return render(request, 'booking/menu.html')

def make_booking(request):
    """Booking view"""
    return render(request, 'booking/booking.html')

def my_bookings(request):
    """My bookings view"""
    return render(request, 'booking/my_bookings.html')

def manage_bookings(request):
    """Manage bookings view"""
    return render(request, 'booking/manage_bookings.html')

def cancel_booking(request, booking_id):
    """Cancel booking view"""
    return render(request, 'booking/cancel_booking.html')

def booking_success(request):
    """Booking success view"""
    return render(request, 'booking/booking_success.html')

def register(request):
    """Register view"""
    return render(request, 'booking/register.html')

def check_availability(request):
    """Check availability view"""
    return render(request, 'booking/check_availability.html')

def admin_dashboard(request):
    """Admin dashboard view"""
    return render(request, 'booking/admin_dashboard.html')

def admin_confirm_booking(request):
    """Admin confirm booking view"""
    return render(request, 'booking/admin_confirm_booking.html')

def admin_cancel_booking(request):
    """Admin cancel booking view"""
    return render(request, 'booking/admin_cancel_booking.html')

def table_management(request):
    """Table management view"""
    return render(request, 'booking/table_management.html')

def edit_table(request):
    """Edit table view"""
    return render(request, 'booking/edit_table.html')


