from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Table(models.Model):
    """Model representing a table in the restaurant"""
    table_number = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    location = models.CharField(
        max_length=50,
        choices=[
            ('WINDOW', 'Window'),
            ('BALCONY', 'Balcony'),
            ('INSIDE', 'Inside'),
            ('BAR', 'Bar Area')
        ]
    )

    def clean(self):
        """Validate table data"""
        if self.table_number <= 0:
            raise ValidationError("Table number must be positive.")
        if self.capacity <= 0:
            raise ValidationError("Table capacity must be positive.")
        if self.capacity > 20:
            raise ValidationError("Table capacity cannot exceed 20 people.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number} (seats {self.capacity})"


class Booking(models.Model):
    """Model representing a booking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    party_size = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled')
        ],
        default='PENDING'
    )

    class Meta:
        # Ensure a table can't be double-booked
        constraints = [
            models.UniqueConstraint(
                fields=['table', 'booking_date', 'booking_time'],
                name='unique_booking'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username}'s booking for {self.party_size} "
            f"on {self.booking_date} at {self.booking_time}"
        )

    def clean(self):
        # Skip validation if table is not assigned yet
        if hasattr(self, 'table') and self.table is not None:
            # Validate the party size doesn't exceed table capacity
            if self.party_size > self.table.capacity:
                raise ValidationError(
                    f"Party size exceeds table capacity "
                    f"({self.table.capacity})"
                )


class MenuItem(models.Model):
    """Model representing an item on the menu"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(
        max_length=50,
        choices=[
            ('STARTER', 'Starter'),
            ('MAIN', 'Main Course'),
            ('DESSERT', 'Dessert'),
            ('DRINK', 'Drink')
        ]
    )
    image = models.ImageField(
        upload_to='menu_items/', blank=True, null=True
    )
    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)

    def clean(self):
        """Validate menu item data"""
        if self.price <= 0:
            raise ValidationError("Price must be positive.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
