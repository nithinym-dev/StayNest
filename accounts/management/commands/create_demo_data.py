from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import OwnerProfile
from properties.models import Property, Room, PropertyImage
from bookings.models import Booking
from payments.models import Payment
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal  # Add this import
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create demo data for testing the hostel booking platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating demo data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            User.objects.filter(is_superuser=False).delete()
            Property.objects.all().delete()
            
        self.stdout.write('Creating demo data...')
        
        # Create demo users
        self.create_demo_users()
        
        # Create demo properties
        self.create_demo_properties()
        
        # Create demo bookings
        self.create_demo_bookings()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created demo data!')
        )

    def create_demo_users(self):
        """Create demo users: admin, owners, and regular users"""
        
        # Create Admin User
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@hostelbook.com',
                password='admin123',
                user_type='admin',
                first_name='System',
                last_name='Administrator',
                phone_number='+91-9999999999',
                is_verified=True,
                is_staff=True
            )
            self.stdout.write(f'Created admin user: {admin_user.username}')

        # Create Owner Users
        owners_data = [
            {
                'username': 'owner1',
                'email': 'owner1@hostelbook.com',
                'password': 'owner123',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'phone_number': '+91-9876543210',
                'business_name': 'Kumar Hospitality Services',
                'document_type': 'pan',
                'document_number': 'ABCDE1234F',
                'business_address': 'MG Road, Bangalore, Karnataka 560001'
            },
            {
                'username': 'owner2', 
                'email': 'owner2@hostelbook.com',
                'password': 'owner123',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'phone_number': '+91-9876543211',
                'business_name': 'Sharma PG & Hostel',
                'document_type': 'aadhaar',
                'document_number': '1234-5678-9012',
                'business_address': 'Koramangala, Bangalore, Karnataka 560034'
            },
            {
                'username': 'owner3',
                'email': 'owner3@hostelbook.com', 
                'password': 'owner123',
                'first_name': 'Amit',
                'last_name': 'Patel',
                'phone_number': '+91-9876543212',
                'business_name': 'Patel Accommodation Hub',
                'document_type': 'business_id',
                'document_number': 'BIZ123456789',
                'business_address': 'Whitefield, Bangalore, Karnataka 560066'
            }
        ]

        for owner_data in owners_data:
            if not User.objects.filter(username=owner_data['username']).exists():
                owner_user = User.objects.create_user(
                    username=owner_data['username'],
                    email=owner_data['email'],
                    password=owner_data['password'],
                    user_type='owner',
                    first_name=owner_data['first_name'],
                    last_name=owner_data['last_name'],
                    phone_number=owner_data['phone_number'],
                    is_verified=True
                )
                
                # Create Owner Profile
                OwnerProfile.objects.create(
                    user=owner_user,
                    business_name=owner_data['business_name'],
                    document_type=owner_data['document_type'],
                    document_number=owner_data['document_number'],
                    business_address=owner_data['business_address'],
                    verification_status='approved'
                )
                
                self.stdout.write(f'Created owner user: {owner_user.username}')

        # Create Regular Users
        users_data = [
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'password': 'user123',
                'first_name': 'Ankit',
                'last_name': 'Singh',
                'phone_number': '+91-9123456789'
            },
            {
                'username': 'user2',
                'email': 'user2@example.com',
                'password': 'user123',
                'first_name': 'Sneha',
                'last_name': 'Reddy',
                'phone_number': '+91-9123456790'
            },
            {
                'username': 'user3',
                'email': 'user3@example.com',
                'password': 'user123',
                'first_name': 'Rohit',
                'last_name': 'Gupta',
                'phone_number': '+91-9123456791'
            },
            {
                'username': 'user4',
                'email': 'user4@example.com',
                'password': 'user123',
                'first_name': 'Kavya',
                'last_name': 'Nair',
                'phone_number': '+91-9123456792'
            }
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    user_type='user',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone_number=user_data['phone_number'],
                    is_verified=True
                )
                self.stdout.write(f'Created regular user: {user.username}')

    def create_demo_properties(self):
        """Create demo properties with rooms"""
        
        owners = User.objects.filter(user_type='owner')
        
        properties_data = [
            {
                'owner': owners[0],
                'name': 'Sunrise Boys Hostel',
                'property_type': 'hostel',
                'description': 'A premium boys hostel located in the heart of MG Road with excellent connectivity to IT parks and educational institutions. Features modern amenities, 24/7 security, and homely food.',
                'address': '123, MG Road, Near Metro Station',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001',
                'latitude': Decimal('12.9716'),
                'longitude': Decimal('77.5946'),
                'wifi': True,
                'meals': True,
                'ac': True,
                'laundry': True,
                'parking': True,
                'security': True,
                'rooms': [
                    {'number': '101', 'type': 'shared', 'capacity': 4, 'daily': 800, 'monthly': 15000, 'deposit': 5000, 'bathroom': True, 'balcony': False},
                    {'number': '102', 'type': 'shared', 'capacity': 3, 'daily': 900, 'monthly': 16000, 'deposit': 5000, 'bathroom': True, 'balcony': True},
                    {'number': '103', 'type': 'private', 'capacity': 1, 'daily': 1500, 'monthly': 25000, 'deposit': 8000, 'bathroom': True, 'balcony': True},
                    {'number': '104', 'type': 'semi_private', 'capacity': 2, 'daily': 1200, 'monthly': 20000, 'deposit': 6000, 'bathroom': True, 'balcony': False},
                ]
            },
            {
                'owner': owners[1],
                'name': 'Pearl Girls PG',
                'property_type': 'pg',
                'description': 'Safe and secure PG accommodation for working women and students. Located in peaceful Koramangala with easy access to major tech companies and shopping centers.',
                'address': '456, 5th Block, Koramangala',
                'city': 'Bangalore',
                'state': 'Karnataka', 
                'pincode': '560034',
                'latitude': Decimal('12.9352'),
                'longitude': Decimal('77.6245'),
                'wifi': True,
                'meals': True,
                'ac': False,
                'laundry': True,
                'parking': False,
                'security': True,
                'rooms': [
                    {'number': '201', 'type': 'shared', 'capacity': 3, 'daily': 750, 'monthly': 14000, 'deposit': 4000, 'bathroom': False, 'balcony': True},
                    {'number': '202', 'type': 'shared', 'capacity': 2, 'daily': 1000, 'monthly': 18000, 'deposit': 5000, 'bathroom': True, 'balcony': True},
                    {'number': '203', 'type': 'private', 'capacity': 1, 'daily': 1800, 'monthly': 28000, 'deposit': 10000, 'bathroom': True, 'balcony': True},
                ]
            },
            {
                'owner': owners[2],
                'name': 'Tech Hub Co-living',
                'property_type': 'hostel',
                'description': 'Modern co-living space designed for young professionals. Located in Whitefield near major IT companies. Features gaming room, gym, and rooftop terrace.',
                'address': '789, ITPL Main Road, Whitefield',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560066',
                'latitude': Decimal('12.9698'),
                'longitude': Decimal('77.7500'),
                'wifi': True,
                'meals': False,
                'ac': True,
                'laundry': True,
                'parking': True,
                'security': True,
                'rooms': [
                    {'number': '301', 'type': 'shared', 'capacity': 4, 'daily': 1200, 'monthly': 22000, 'deposit': 8000, 'bathroom': True, 'balcony': False},
                    {'number': '302', 'type': 'private', 'capacity': 1, 'daily': 2000, 'monthly': 35000, 'deposit': 12000, 'bathroom': True, 'balcony': True},
                    {'number': '303', 'type': 'semi_private', 'capacity': 2, 'daily': 1500, 'monthly': 28000, 'deposit': 10000, 'bathroom': True, 'balcony': True},
                ]
            },
            {
                'owner': owners[0],
                'name': 'Green Valley Hostel',
                'property_type': 'hostel',
                'description': 'Eco-friendly hostel surrounded by greenery in Electronic City. Perfect for IT professionals with shuttle service to major tech parks.',
                'address': '321, Electronic City Phase 1',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560100',
                'latitude': Decimal('12.8456'),
                'longitude': Decimal('77.6603'),
                'wifi': True,
                'meals': True,
                'ac': False,
                'laundry': True,
                'parking': True,
                'security': True,
                'rooms': [
                    {'number': '401', 'type': 'shared', 'capacity': 6, 'daily': 600, 'monthly': 12000, 'deposit': 3000, 'bathroom': False, 'balcony': False},
                    {'number': '402', 'type': 'shared', 'capacity': 4, 'daily': 700, 'monthly': 13000, 'deposit': 4000, 'bathroom': True, 'balcony': False},
                    {'number': '403', 'type': 'private', 'capacity': 1, 'daily': 1300, 'monthly': 22000, 'deposit': 7000, 'bathroom': True, 'balcony': True},
                ]
            },
            {
                'owner': owners[1],
                'name': 'Metro Connect PG',
                'property_type': 'pg',
                'description': 'Conveniently located PG near Indiranagar Metro Station. Ideal for both men and women with separate floors and common areas.',
                'address': '654, 100 Feet Road, Indiranagar',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560038',
                'latitude': Decimal('12.9719'),
                'longitude': Decimal('77.6412'),
                'wifi': True,
                'meals': True,
                'ac': True,
                'laundry': False,
                'parking': False,
                'security': True,
                'rooms': [
                    {'number': '501', 'type': 'shared', 'capacity': 3, 'daily': 850, 'monthly': 16000, 'deposit': 5000, 'bathroom': False, 'balcony': True},
                    {'number': '502', 'type': 'semi_private', 'capacity': 2, 'daily': 1100, 'monthly': 19000, 'deposit': 6000, 'bathroom': True, 'balcony': True},
                ]
            }
        ]

        for prop_data in properties_data:
            if not Property.objects.filter(name=prop_data['name']).exists():
                property_obj = Property.objects.create(
                    owner=prop_data['owner'],
                    name=prop_data['name'],
                    property_type=prop_data['property_type'],
                    description=prop_data['description'],
                    address=prop_data['address'],
                    city=prop_data['city'],
                    state=prop_data['state'],
                    pincode=prop_data['pincode'],
                    latitude=prop_data['latitude'],
                    longitude=prop_data['longitude'],
                    wifi=prop_data['wifi'],
                    meals=prop_data['meals'],
                    ac=prop_data['ac'],
                    laundry=prop_data['laundry'],
                    parking=prop_data['parking'],
                    security=prop_data['security'],
                    is_active=True
                )

                # Create rooms for this property
                for room_data in prop_data['rooms']:
                    Room.objects.create(
                        property_obj=property_obj,
                        room_number=room_data['number'],
                        room_type=room_data['type'],
                        capacity=room_data['capacity'],
                        current_occupancy=random.randint(0, room_data['capacity']-1),
                        daily_rate=Decimal(str(room_data['daily'])),
                        monthly_rate=Decimal(str(room_data['monthly'])),
                        security_deposit=Decimal(str(room_data['deposit'])),
                        attached_bathroom=room_data['bathroom'],
                        balcony=room_data['balcony'],
                        is_available=True
                    )

                self.stdout.write(f'Created property: {property_obj.name} with {len(prop_data["rooms"])} rooms')

    def create_demo_bookings(self):
        """Create demo bookings"""
        
        users = User.objects.filter(user_type='user')
        rooms = Room.objects.all()
        
        if not users.exists() or not rooms.exists():
            return

        # Create various types of bookings
        booking_scenarios = [
            {
                'user': users[0],
                'room': rooms[0],
                'booking_type': 'monthly',
                'days_from_now': -15,
                'duration': 30,
                'status': 'confirmed',
                'guests': 1
            },
            {
                'user': users[1],
                'room': rooms[2],
                'booking_type': 'daily',
                'days_from_now': -5,
                'duration': 7,
                'status': 'completed',
                'guests': 1
            },
            {
                'user': users[2],
                'room': rooms[4],
                'booking_type': 'monthly',
                'days_from_now': 5,
                'duration': 30,
                'status': 'pending',
                'guests': 2
            },
            {
                'user': users[3],
                'room': rooms[1],
                'booking_type': 'daily',
                'days_from_now': -2,
                'duration': 3,
                'status': 'confirmed',
                'guests': 1
            },
            {
                'user': users[0],
                'room': rooms[3],
                'booking_type': 'daily',
                'days_from_now': 10,
                'duration': 5,
                'status': 'pending',
                'guests': 1
            }
        ]

        for scenario in booking_scenarios:
            check_in_date = timezone.now().date() + timedelta(days=scenario['days_from_now'])
            check_out_date = check_in_date + timedelta(days=scenario['duration'])
            
            if not Booking.objects.filter(
                user=scenario['user'],
                room=scenario['room'],
                check_in_date=check_in_date
            ).exists():
                
                # Calculate amounts using Decimal arithmetic
                if scenario['booking_type'] == 'daily':
                    base_amount = scenario['room'].daily_rate * Decimal(str(scenario['duration']))
                else:
                    # Convert division to Decimal
                    days_ratio = Decimal(str(scenario['duration'])) / Decimal('30')
                    base_amount = scenario['room'].monthly_rate * days_ratio
                
                booking = Booking.objects.create(
                    user=scenario['user'],
                    room=scenario['room'],
                    booking_type=scenario['booking_type'],
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    guests=scenario['guests'],
                    base_amount=base_amount,
                    security_deposit=scenario['room'].security_deposit,
                    total_amount=base_amount + scenario['room'].security_deposit,
                    status=scenario['status'],
                    special_requests=f"Demo booking for testing - {scenario['booking_type']} stay"
                )

                # Create payment record for confirmed bookings
                if scenario['status'] in ['confirmed', 'completed']:
                    Payment.objects.create(
                        booking=booking,
                        razorpay_order_id=f'order_demo_{booking.id}_{random.randint(1000, 9999)}',
                        razorpay_payment_id=f'pay_demo_{booking.id}_{random.randint(1000, 9999)}',
                        amount=booking.total_amount,
                        status='completed'
                    )

                self.stdout.write(f'Created booking: {booking.id} for {scenario["user"].username}')
