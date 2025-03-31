from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Table(models.Model):
    """Model representing a table in the restaurant"""
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=50, choices=[
        ('WINDOW', 'Window'),
        ('BALCONY', 'Balcony'),
        ('INSIDE', 'Inside'),
        ('BAR', 'Bar Area')
    ])
    
    def __str__(self):
        return f"Table {self.table_number} (seats {self.capacity})"