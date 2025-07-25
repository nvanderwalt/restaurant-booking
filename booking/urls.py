from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('book/', views.make_booking, name='make_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path(
        'cancel-booking/<int:booking_id>/',
        views.cancel_booking,
        name='cancel_booking'
    ),
    path(
        'booking-success/',
        views.booking_success,
        name='booking_success'
    ),
    path(
        'check-availability/',
        views.check_availability,
        name='check_availability'
    ),

    # Restaurant owner admin views
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),
    path(
        'admin-tables/',
        views.table_management,
        name='table_management'
    ),
    path(
        'admin-tables/add/',
        views.edit_table,
        name='add_table'
    ),
    path(
        'admin-tables/edit/<int:table_id>/',
        views.edit_table,
        name='edit_table'
    ),
    path(
        'admin-confirm-booking/<int:booking_id>/',
        views.admin_confirm_booking,
        name='admin_confirm_booking'
    ),
    path(
        'admin-cancel-booking/<int:booking_id>/',
        views.admin_cancel_booking,
        name='admin_cancel_booking'
    ),
    path(
        'delete-table/<int:table_id>/',
        views.delete_table,
        name='delete_table'
    ),

    # Menu management
    path(
        'admin-menu/',
        views.menu_management,
        name='menu_management'
    ),
    path(
        'admin-menu/add/',
        views.edit_menu_item,
        name='add_menu_item'
    ),
    path(
        'admin-menu/edit/<int:item_id>/',
        views.edit_menu_item,
        name='edit_menu_item'
    ),
    path(
        'delete-menu-item/<int:item_id>/',
        views.delete_menu_item,
        name='delete_menu_item'
    ),

    # Booking management
    path(
        'manage-bookings/',
        views.manage_bookings,
        name='manage_bookings'
    ),
]
