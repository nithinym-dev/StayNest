# HostelBook - Property Management System

![HostelBook Logo](static/images/logo.png)

## Overview

HostelBook is a comprehensive property management system designed specifically for hostels and PG accommodations. It provides a robust platform for property owners to manage their properties and for users to find and book accommodations seamlessly.

## Features

### For Property Owners
- **Property Management**
  - Add and manage multiple properties
  - Upload property images with automatic primary image selection
  - Set detailed property information including amenities
  - Real-time location mapping using OpenStreetMap
  - Track property status and occupancy

- **Room Management**
  - Create and manage multiple room types
  - Set room capacities and pricing
  - Track room availability
  - Manage room amenities
  - Monitor occupancy rates

- **Booking Management**
  - View and manage bookings
  - Track payment status
  - Handle check-in/check-out
  - Manage cancellations

### For Users
- **Property Search**
  - Advanced search filters
  - Location-based search
  - Price range filtering
  - Amenity-based filtering

- **Booking System**
  - Real-time availability checking
  - Secure payment processing
  - Booking confirmation
  - Booking history

### System Features
- User authentication and authorization
- Owner verification system
- Secure payment integration
- Responsive design
- Real-time notifications
- Interactive maps

## Technology Stack

- **Backend**
  - Django 4.2+
  - Python 3.10+
  - SQLite3 (Development)
  - PostgreSQL (Production Ready)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
  - Font Awesome Icons

- **Maps**
  - OpenStreetMap
  - Leaflet.js

- **Security**
  - Django Security Middleware
  - CSRF Protection
  - XSS Protection
  - Secure Password Hashing

## Installation

1. Clone the repository (Requires Permission)
```bash
git clone [repository-url]
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## Configuration

### Required Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `EMAIL_HOST`: SMTP host for emails
- `EMAIL_PORT`: SMTP port
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password

## Usage

### Admin Dashboard
- Access the admin interface at `/admin`
- Manage users, properties, and bookings
- Handle owner verifications
- Monitor system activity

### Property Management
1. Register as an owner
2. Submit verification documents
3. Add properties and rooms
4. Manage bookings and payments

### Booking Process
1. Search for properties
2. View property details
3. Check room availability
4. Make a booking
5. Process payment
6. Receive confirmation
