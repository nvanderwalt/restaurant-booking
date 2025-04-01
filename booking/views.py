
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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
    """Display the restaurant menu"""
    starters = MenuItem.objects.filter(category='STARTER')
    mains = MenuItem.objects.filter(category='MAIN')
    desserts = MenuItem.objects.filter(category='DESSERT')
    drinks = MenuItem.objects.filter(category='DRINK')
    
    context = {
        'starters': starters,
        'mains': mains,
        'desserts': desserts,
        'drinks': drinks
    }
    return render(request, 'booking/menu.html', context)

def make_booking(request):
    
    return render(request, 'booking/booking.html')

def my_bookings(request):
    
    return render(request, 'booking/my_bookings.html')

def manage_bookings(request):
    
    return render(request, 'booking/manage_bookings.html')

def cancel_booking(request, booking_id):
    
    return render(request, 'booking/cancel_booking.html')

def booking_success(request):
    
    return render(request, 'booking/booking_success.html')

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def check_availability(request):
    
    return render(request, 'booking/check_availability.html')

def admin_dashboard(request):
    
    return render(request, 'booking/admin_dashboard.html')

def admin_confirm_booking(request):
    
    return render(request, 'booking/admin_confirm_booking.html')

def admin_cancel_booking(request):
    
    return render(request, 'booking/admin_cancel_booking.html')

def table_management(request):
    
    return render(request, 'booking/table_management.html')

def edit_table(request):
    
    return render(request, 'booking/edit_table.html')


