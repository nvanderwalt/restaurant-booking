from django.contrib import admin
from .models import Booking, Table, MenuItem


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'location')
    list_filter = ('location', 'capacity')
    search_fields = ('table_number',)
    ordering = ('table_number',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'vegetarian', 'vegan', 'gluten_free'
    )
    list_filter = ('category', 'vegetarian', 'vegan', 'gluten_free')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')
    list_editable = ('price', 'vegetarian', 'vegan', 'gluten_free')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'table', 'booking_date', 'booking_time', 'party_size',
        'status'
    )
    list_filter = (
        'status', 'booking_date', 'booking_time', 'table__location'
    )
    search_fields = ('user__username', 'user__email', 'notes')
    ordering = ('-booking_date', '-booking_time')
    list_editable = ('status',)
    date_hierarchy = 'booking_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'table')
