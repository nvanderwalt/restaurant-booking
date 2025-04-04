import os
import django
import random
from datetime import datetime, timedelta, time
from decimal import Decimal


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_booking.settings')
django.setup()

from booking.models import Table, MenuItem
from django.contrib.auth.models import User

def create_tables():
    """Create sample tables"""
    print("Creating tables...")
    
    # Delete existing tables
    Table.objects.all().delete()
    print("Deleted existing tables")
    
    tables_data = [
        # Table number, capacity, location
        (1, 2, 'WINDOW'),
        (2, 2, 'WINDOW'),
        (3, 4, 'WINDOW'),
        (4, 4, 'INSIDE'),
        (5, 6, 'INSIDE'),
        (6, 8, 'INSIDE'),
        (7, 2, 'BALCONY'),
        (8, 4, 'BALCONY'),
        (9, 6, 'BALCONY'),
        (10, 2, 'BAR'),
        (11, 2, 'BAR'),
        (12, 4, 'BAR'),
    ]
    
    # Create each table
    for table_number, capacity, location in tables_data:
        Table.objects.create(
            table_number=table_number,
            capacity=capacity,
            location=location
        )
    
    print(f"Created {len(tables_data)} tables")

def create_menu_items():
    """Create sample menu items"""
    print("Creating menu items...")
    
    # Delete existing menu items
    MenuItem.objects.all().delete()
    print("Deleted existing menu items")
    
    # Starters
    starters = [
        {
            'name': 'Bruschetta',
            'description': 'Grilled bread rubbed with garlic and topped with diced tomatoes, fresh basil, and olive oil.',
            'price': Decimal('8.99'),
            'vegetarian': True,
            'vegan': True,
            'gluten_free': False
        },
        {
            'name': 'Caprese Salad',
            'description': 'Fresh mozzarella, tomatoes, and sweet basil, seasoned with salt and olive oil.',
            'price': Decimal('10.50'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': True
        },
        {
            'name': 'Fried Calamari',
            'description': 'Tender calamari lightly fried to golden perfection. Served with marinara sauce.',
            'price': Decimal('12.99'),
            'vegetarian': False,
            'vegan': False,
            'gluten_free': False
        },
        {
            'name': 'Garlic Bread',
            'description': 'Italian bread topped with garlic butter and toasted to perfection.',
            'price': Decimal('5.99'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': False
        },
    ]
    
    # Main courses
    mains = [
        {
            'name': 'Spaghetti Carbonara',
            'description': 'Classic Italian pasta dish with eggs, cheese, pancetta and black pepper.',
            'price': Decimal('16.99'),
            'vegetarian': False,
            'vegan': False,
            'gluten_free': False
        },
        {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza with tomato sauce, mozzarella, and fresh basil.',
            'price': Decimal('14.50'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': False
        },
        {
            'name': 'Veal Parmigiana',
            'description': 'Breaded veal cutlet topped with tomato sauce and melted mozzarella cheese.',
            'price': Decimal('22.99'),
            'vegetarian': False,
            'vegan': False,
            'gluten_free': False
        },
        {
            'name': 'Risotto ai Funghi',
            'description': 'Creamy Arborio rice with porcini mushrooms and Parmesan cheese.',
            'price': Decimal('18.50'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': True
        },
        {
            'name': 'Grilled Salmon',
            'description': 'Fresh salmon fillet grilled with lemon and herbs. Served with seasonal vegetables.',
            'price': Decimal('24.99'),
            'vegetarian': False,
            'vegan': False,
            'gluten_free': True
        },
        {
            'name': 'Eggplant Parmigiana',
            'description': 'Layers of eggplant, tomato sauce, mozzarella, and Parmesan cheese.',
            'price': Decimal('17.99'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': True
        },
    ]
    
    # Desserts
    desserts = [
        {
            'name': 'Tiramisu',
            'description': 'Classic Italian dessert made with layers of coffee-soaked ladyfingers and mascarpone cream.',
            'price': Decimal('8.99'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': False
        },
        {
            'name': 'Panna Cotta',
            'description': 'Italian custard dessert topped with berry compote.',
            'price': Decimal('7.50'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': True
        },
        {
            'name': 'Cannoli',
            'description': 'Crisp pastry tubes filled with sweet ricotta cream and chocolate chips.',
            'price': Decimal('6.99'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': False
        },
        {
            'name': 'Gelato Selection',
            'description': 'Choice of three scoops from our daily selection of authentic Italian gelato.',
            'price': Decimal('9.50'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': True
        },
    ]
    
    # Drinks
    drinks = [
        {
            'name': 'Espresso',
            'description': 'Strong Italian coffee served in a small cup.',
            'price': Decimal('3.50'),
            'vegetarian': True,
            'vegan': True,
            'gluten_free': True
        },
        {
            'name': 'Cappuccino',
            'description': 'Espresso coffee topped with steamed milk foam.',
            'price': Decimal('4.50'),
            'vegetarian': True,
            'vegan': False,
            'gluten_free': True
        },
        {
            'name': 'House Red Wine',
            'description': 'Glass of our premium house red wine.',
            'price': Decimal('7.99'),
            'vegetarian': True,
            'vegan': True,
            'gluten_free': True
        },
        {
            'name': 'House White Wine',
            'description': 'Glass of our premium house white wine.',
            'price': Decimal('7.99'),
            'vegetarian': True,
            'vegan': True,
            'gluten_free': True
        },
        {
            'name': 'Aperol Spritz',
            'description': 'Refreshing cocktail made with Aperol, Prosecco, and soda water.',
            'price': Decimal('9.50'),
            'vegetarian': True,
            'vegan': True,
            'gluten_free': True
        },
        {
            'name': 'San Pellegrino Sparkling Water',
            'description': '750ml bottle of premium Italian sparkling water.',
            'price': Decimal('4.99'),
            'vegetarian': True,
            'vegan': True,
            'gluten_free': True
        },
    ]
    
    # Add items to DB
    for item in starters:
        MenuItem.objects.create(category='STARTER', **item)
    
    for item in mains:
        MenuItem.objects.create(category='MAIN', **item)
    
    for item in desserts:
        MenuItem.objects.create(category='DESSERT', **item)
    
    for item in drinks:
        MenuItem.objects.create(category='DRINK', **item)
    
    print(f"Created {len(starters)} starters, {len(mains)} main courses, {len(desserts)} desserts, and {len(drinks)} drinks")

if __name__ == '__main__':
    # Create
    create_tables()
    create_menu_items()
    
    print("Sample data creation complete!")