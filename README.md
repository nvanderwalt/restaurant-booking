# La Dolce Vita Restaurant Booking System

A comprehensive restaurant booking application that allows customers to browse menus, make table reservations and manage their bookings, while providing restaurant staff with tools to manage tables, menus, and bookings.

## Table of Contents

1. [User Experience (UX)](#user-experience-ux)
2. [Features](#features)
3. [Database Design](#database-design)
4. [Technologies Used](#technologies-used)
5. [Testing](#testing)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Live Demo](#live-demo)
9. [Future Features](#future-features)
10. [Credits](#credits)

## User Experience (UX)

### Strategy
#### Project Goals
This project aims to create a full-featured restaurant booking system that:
- Allows customers to view the restaurant's menu
- Enables users to make, view, edit and cancel reservations
- Provides restaurant staff with tools to manage tables, menu items, and bookings
- Creates a responsive experience that works across all devices

#### User Stories
##### As a site visitor, I want to:
- View the restaurant's menu to decide if I want to dine there
- Understand the restaurant's opening hours and contact information
- Create an account so I can make reservations

##### As a registered user, I want to:
- Make a reservation by selecting date, time, and party size
- View all my upcoming reservations in one place
- Edit my reservations if my plans change
- Cancel reservations I no longer need
- Be notified of successful actions (booking confirmation, changes, cancellations)

##### As restaurant staff, I want to:
- View all upcoming reservations
- Confirm or cancel customer bookings
- Add, edit and remove menu items
- Configure restaurant table layouts and capacities

### Scope
The project includes the following features:

#### Must-have features:
- registration and authentication
- Reservation booking system with date/time selection
- Table availability checking
- Viewing and managing reservations
- Menu display
- Admin dashboard for restaurant management

#### Should-have features:
- Mobile-responsive design
- Form validation with clear feedback
- User-friendly interface with Bootstrap styling
- Success/error notifications

#### Could-have features:
- Email notifications for booking confirmations
- Restaurant layout visualization
- Customer reviews and ratings

### Structure
The application follows Django's MVT (Model-View-Template) architecture and is structured as follows:

- Models: Define the database structure for bookings, tables, menu items
- Views: Handle the logic for processing user requests and returning appropriate responses
- Templates: Present the data to users with responsive design

Navigation is intuitive, with a consistent header and footer across all pages. The booking workflow guides users through the reservation process with clear steps and feedback.





### Desktop Page:

<img src="screenshots/desktop_homepage.png" alt="Home page">
<br/>
<img src="screenshots/desktop_menupage.png" alt="Menu page">
<br/>
<img src="screenshots/desktop_bookingpage.png" alt="booking page">
<br/>
<img src="screenshots/desktop_admindashboardpage.png" alt=Admin Dashboard page">

### Mobile Page:

<img src="screenshots/mobile_homepage.png" alt="Home page">
<br/>
<img src="screenshots/mobile_menupage.png" alt="Menu page">
<br/>
<img src="screenshots/mobile_bookingpage.png" alt="booking page">


### Surface
The website uses a warm, inviting color palette that conveys an elegant Italian dining experience:
- Primary colors: Dark and mordern tones
- Secondary colors: Green and Yellow for navigation mobility


## Features

### Customer Features

- **User Registration and Authentication**: Create an account, log in, and manage your profile
- **Menu Browsing**: View the restaurant's menu items by category (starters, mains, desserts, drinks)
- **Table Booking**: Make a reservation by selecting date, time, and party size
- **Real-time Availability**: Check available tables based on selected date, time, and party size
- **Booking Management**: View, manage, and cancel your bookings


### Restaurant Administration Features

- **Dashboard**: Overview of bookings, tables, and menu items
- **Booking Management**: View, confirm, and cancel customer bookings
- **Menu Management**: Add, edit, and delete menu items with dietary information
- **Table Management**: Configure restaurant tables with various capacities and locations


### Technical Features

- Responsive design using Bootstrap 5
- Form validation with clear user feedback
- Database model constraints to prevent double bookings
- Secure authentication system
- Dynamic content loading

## Technologies Used

### Languages
- HTML5
- CSS3
- JavaScript
- Python 3.12

### Frameworks and Libraries
- Django 5.1.7: Main web framework
- Bootstrap 5: Front-end framework for responsive design
- JavaScript library
- Django Crispy Forms: For rendering beautiful forms
- Whitenoise: Static file serving

### Database
- SQLite: Development database
- PostgreSQL: Production database

### Tools
- Git: Version control
- GitHub: Code hosting platform
- Heroku: Cloud platform for deployment
- VS Code: Code editor

## Testing

### Automated Testing
Automated tests have been implemented to verify key functionality of the application:
```bash
# Example tests from test_views.py
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
Ran 7 tests in 6.479s

OK
Destroying test database for alias 'default'...
```

### Form Testing
```bash
# Example tests from test_forms.py
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
Ran 7 tests in 2.222s

OK
Destroying test database for alias 'default'...
```

### Manual Testing
| Feature | Test Case | Result |
|---------|-----------|--------|
| User Registration | Create new account with valid data | ✅ Pass |
| | Try to register with existing username | ✅ Pass |
| | Try to register with mismatched passwords | ✅ Pass |
| Login | Login with valid credentials | ✅ Pass |
| | Login with invalid credentials | ✅ Pass |
| Booking Creation | Create booking with valid data | ✅ Pass |
| | Try to book in the past | ✅ Pass |
| | Try to submit form with missing fields | ✅ Pass |
| | Check availability shows correct tables | ✅ Pass |
| Booking Management | View list of own bookings | ✅ Pass |
| | Cancel booking | ✅ Pass |
| Menu Display | View menu categories and items | ✅ Pass |
| | Verify dietary information shows correctly | ✅ Pass |
| Admin Features | Add new menu item | ✅ Pass |
| | Edit table information | ✅ Pass |
| | Confirm customer booking | ✅ Pass |
| | View booking statistics | ✅ Pass |
| Responsive Design | Test on mobile device (iPhone) | ✅ Pass |
| | Test on tablet device (iPad) | ✅ Pass |
| | Test on desktop | ✅ Pass |

### Browser Compatibility
| Browser | Version | Result |
|---------|---------|--------|
| Chrome | Latest | ✅ Compatible |
| Firefox | Latest | ✅ Compatible |
| Safari | Latest | ✅ Compatible |
| Edge | Latest | ✅ Compatible |

## Database Design
- The application uses a relational database with the following models:

### Table Model
- table_number: Unique identifier for each table
- capacity: Maximum number of guests the table can accommodate
- location: Position within the restaurant (Window, Inside, Balcony, Bar)

### Booking Model
- Foreign key to Django's User model
- table: Foreign key to Table model
- booking_date: Date of reservation
- booking_time: Time of reservation
- party_size: Number of guests
- notes: Optional additional information
- status: Current status (Pending, Confirmed, Cancelled)
- created_on: Automatic timestamp
- updated_on: Automatic timestamp when modified

### MenuItem Model
- name: Name of the dish
- description: Detailed description
- price: Cost in decimal format
- category: Type of item (Starter, Main, Dessert, Drink)
- image: Optional photo of the dish
- vegetarian: Boolean field
- vegan: Boolean field
- gluten_free: Boolean field

## Installation




### Local Development

1. Clone the repository:

```bash
git clone https://github.com/nvanderwalt/restaurant-booking.git
cd restaurant-booking
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  
# On Windows: 
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Setup the database:

```bash
python manage.py migrate
```

5. Create a superuser (for admin access):

```bash
python manage.py createsuperuser
```

6. Load sample data (optional):

```bash
python load_sample_data.py
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Access the application at http://127.0.0.1:8000/

### Heroku Deployment
1. Create a Heroku account and create a new app
2. In the Heroku dashboard, go to the "Resources" tab and add the Heroku Postgres add-on
3. In the "Settings" tab, click "Reveal Config Vars" and add the following:

- SECRET_KEY: Your secret key
- DISABLE_COLLECTSTATIC: 0
4. Create a Procfile in your root directory with the following content:
```bash
web: gunicorn restaurant_booking.wsgi:application
```
5. Update settings.py for production:
```bash
import dj_database_url

DEBUG = 'DEBUG' in os.environ

ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'localhost']

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}
```
6. Install Heroku CLI and login:
```bash
heroku login
```
7. Initialize a git repository (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
```
8. Add Heroku remote:
```bash
heroku git:remote -a your-app-name
```
9. Push to Heroku:
```bash
git push heroku main
```
10. Run migrations on Heroku:
```bash
heroku run python manage.py migrate
```
11. Create a superuser on Heroku:
```bash
heroku run python manage.py createsuperuser
```

## Usage

### Making a Booking

1. Create an account or log in
2. Navigate to "Book a Table"
3. Select date, time, and party size
4. Click "Check Availability"
5. Choose an available table
6. Confirm your booking

### Admin Access

1. Log in with superuser credentials
2. Access the admin dashboard at /admin-dashboard/
3. Manage bookings, tables, and menu items

## Live Demo

You can explore a live version of the application [here](https://restaurantbooking-b53ee86d5fcb.herokuapp.com/).

## Future Features

- Email notifications for booking confirmations and reminders
- Integration with payment gateway for deposits
- Online ordering system for takeaway
- Customer loyalty program
- Customizable table layout visualization
- Special events and promotions management

## Credits

- Bootstrap for the responsive framework
- Django documentation and community for development guidance
- Unsplash for stock photography

