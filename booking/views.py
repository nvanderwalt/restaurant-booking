from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count, Sum
from django.views.decorators.http import require_POST
from django.db.models import Q
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

@login_required
def make_booking(request):
    #booking submission
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            
            # Get table
            table_id = request.POST.get('table_id')
            if not table_id:
                messages.error(request, 'Please select a table')
                return render(request, 'booking/booking.html', {'form': form})
            
            booking.table = get_object_or_404(Table, id=table_id)
            
            # Check if booking available
            existing_bookings = Booking.objects.filter(
                table=booking.table,
                booking_date=booking.booking_date,
                booking_time=booking.booking_time,
                status__in=['PENDING', 'CONFIRMED']
            )
            
            if existing_bookings.exists():
                messages.error(request, 'Sorry, this table is not available.')
                return render(request, 'booking/booking.html', {'form': form})
            
            # Save
            booking.status = 'PENDING'
            booking.save()
            
            messages.success(request, 'Your booking has been submitted and is pending confirmation.')
            return redirect('booking_success')
    else:
        form = BookingForm()
    
    return render(request, 'booking/booking.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date', '-booking_time')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

def manage_bookings(request):
    
    return render(request, 'booking/manage_bookings.html')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'CANCELLED':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, 'Your booking has been cancelled successfully.')
    else:
        messages.info(request, 'This booking is already cancelled.')
    
    return redirect('my_bookings')

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

@require_POST
def check_availability(request):
    date = request.POST.get('booking_date')
    time = request.POST.get('booking_time')
    party_size = int(request.POST.get('party_size', 0))
    
    # Get all tables that can accommodate the party size
    potential_tables = Table.objects.filter(capacity__gte=party_size)
    
    # Get tables that are already booked at this time
    booked_tables = Booking.objects.filter(
        booking_date=date,
        booking_time=time,
        status__in=['PENDING', 'CONFIRMED']
    ).values_list('table_id', flat=True)
    
    # Filter out booked tables
    available_tables = potential_tables.exclude(id__in=booked_tables)
    
    # Convert to list for JSON response
    tables_data = [
        {
            'id': table.id,
            'table_number': table.table_number,
            'capacity': table.capacity,
            'location': table.get_location_display()
        }
        for table in available_tables
    ]
    
    return JsonResponse({'available_tables': tables_data})

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # booking statistics
    pending_count = Booking.objects.filter(status='PENDING').count()
    confirmed_count = Booking.objects.filter(status='CONFIRMED').count()
    todays_count = Booking.objects.filter(
        booking_date=timezone.now().date(),
        status__in=['PENDING', 'CONFIRMED']
    ).count()
    
    # table statistics
    table_count = Table.objects.count()
    total_capacity = Table.objects.aggregate(total=Sum('capacity'))['total'] or 0
    
    # menu statistics
    menu_item_count = MenuItem.objects.count()
    
    # recent bookings
    recent_bookings = Booking.objects.all().order_by('-booking_date', '-booking_time')[:10]
    
    context = {
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'todays_count': todays_count,
        'table_count': table_count,
        'total_capacity': total_capacity,
        'menu_item_count': menu_item_count,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'admin/dashboard.html', context)

@staff_member_required
def admin_confirm_booking(request, booking_id):
    """Admin confirm booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'PENDING':
        booking.status = 'CONFIRMED'
        booking.save()
        messages.success(request, f'Booking for {booking.user.username} has been confirmed.')
    else:
        messages.warning(request, 'This booking cannot be confirmed.')
    
    return redirect('admin_dashboard')

@staff_member_required
def admin_cancel_booking(request, booking_id):
    """Admin cancel booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status != 'CANCELLED':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, f'Booking for {booking.user.username} has been cancelled.')
    else:
        messages.info(request, 'This booking is already cancelled.')
    
    return redirect('admin_dashboard')

@staff_member_required
def table_management(request):
    """Table management view"""
    tables = Table.objects.all().order_by('table_number')
    return render(request, 'admin/table_management.html', {'tables': tables})

@staff_member_required
def edit_table(request, table_id=None):
    """Add/Edit table view"""
    table = None
    if table_id:
        table = get_object_or_404(Table, id=table_id)
    
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            action = 'updated' if table else 'added'
            messages.success(request, f'Table successfully {action}.')
            return redirect('table_management')
    else:
        form = TableForm(instance=table)
    
    return render(request, 'admin/edit_table.html', {'form': form, 'table': table})


@staff_member_required
@require_POST
def delete_table(request, table_id):
    """Delete table"""
    table = get_object_or_404(Table, id=table_id)
    table_number = table.table_number
    table.delete()
    messages.success(request, f'Table {table_number} has been deleted.')
    return redirect('table_management')

#menu management functions
@staff_member_required
def menu_management(request):
    """Menu management view"""
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
    return render(request, 'admin/menu_management.html', context)

@staff_member_required
def edit_menu_item(request, item_id=None):
    """Add/Edit menu item view"""
    menu_item = None
    if item_id:
        menu_item = get_object_or_404(MenuItem, id=item_id)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            action = 'updated' if menu_item else 'added'
            messages.success(request, f'Menu item successfully {action}.')
            return redirect('menu_management')
    else:
        form = MenuItemForm(instance=menu_item)
    
    return render(request, 'admin/edit_menu_item.html', {'form': form, 'menu_item': menu_item})

@staff_member_required
@require_POST
def delete_menu_item(request, item_id):
    """Delete menu item"""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    item_name = menu_item.name
    menu_item.delete()
    messages.success(request, f'Menu item "{item_name}" has been deleted.')
    return redirect('menu_management')