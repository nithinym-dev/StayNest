from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from properties.models import Room
from .models import Booking
from .forms import BookingForm
import razorpay
from django.conf import settings
from decimal import Decimal


# @login_required
# def book_room(request, room_id):
#     room = get_object_or_404(Room, id=room_id)
    
#     if request.user.user_type != 'user':
#         messages.error(request, 'Only users can make bookings.')
#         return redirect('property_detail', pk=room.property_obj.pk)  # Updated here too
    
#     if room.available_spots <= 0:
#         messages.error(request, 'This room is fully occupied.')
#         return redirect('property_detail', pk=room.property_obj.pk)  # Updated 
    
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.room = room
#             booking.security_deposit = room.security_deposit
#             booking.save()
            
#             # Create Razorpay order
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
#             amount = int(booking.total_amount * 100)  # Convert to paise
#             order_data = {
#                 'amount': amount,
#                 'currency': 'INR',
#                 'receipt': f'booking_{booking.id}',
#                 'payment_capture': 1
#             }
            
#             order = client.order.create(order_data)
            
#             # Create payment record
#             from payments.models import Payment
#             Payment.objects.create(
#                 booking=booking,
#                 razorpay_order_id=order['id'],
#                 amount=booking.total_amount,
#             )
            
#             return redirect('process_payment', booking_id=booking.id)
#     else:
#         form = BookingForm()
    
#     context = {
#         'form': form,
#         'room': room,
#     }
#     return render(request, 'bookings/book_room.html', context)



@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.user.user_type != 'user':
        messages.error(request, 'Only users can make bookings.')
        return redirect('property_detail', pk=room.property_obj.pk)
    
    if room.available_spots <= 0:
        messages.error(request, 'This room is fully occupied.')
        return redirect('property_detail', pk=room.property_obj.pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.security_deposit = room.security_deposit
            
            # Let the model calculate base_amount and total_amount
            booking.base_amount = Decimal('0')  # Will be calculated in save()
            booking.total_amount = Decimal('0')  # Will be calculated in save()
            
            booking.save()
            
            # Create Razorpay order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            amount = int(booking.total_amount * 100)  # Convert to paise
            order_data = {
                'amount': amount,
                'currency': 'INR',
                'receipt': f'booking_{booking.id}',
                'payment_capture': 1
            }
            
            order = client.order.create(order_data)
            
            # Create payment record
            from payments.models import Payment
            Payment.objects.create(
                booking=booking,
                razorpay_order_id=order['id'],
                amount=booking.total_amount,
            )
            
            return redirect('process_payment', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'bookings/book_room.html', context)


@login_required
def booking_list(request):
    bookings = request.user.bookings.all().order_by('-created_at')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})
