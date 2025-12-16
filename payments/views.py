from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import razorpay
import json
from .models import Payment
from bookings.models import Booking

@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    
    context = {
        'booking': booking,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': int(payment.amount * 100),  # Convert to paise
    }
    
    return render(request, 'payments/process_payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            # Get payment details from frontend
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            
            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            
            # Update payment record
            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'completed'
            payment.save()
            
            # Update booking status
            booking = payment.booking
            booking.status = 'confirmed'
            booking.save()
            
            # Update room occupancy
            room = booking.room
            room.current_occupancy += booking.guests
            room.save()
            
            messages.success(request, 'Payment successful! Your booking has been confirmed.')
            return redirect('booking_detail', booking_id=booking.id)
            
        except Exception as e:
            messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('dashboard')
    
    return redirect('dashboard')

@csrf_exempt
def payment_failure(request):
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('dashboard')
