from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import User, OwnerProfile
from .forms import UserRegistrationForm, OwnerRegistrationForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {}
    if request.user.user_type == 'admin':
        context['pending_owners'] = OwnerProfile.objects.filter(verification_status='pending')
    elif request.user.user_type == 'owner':
        context['properties'] = request.user.properties.all()
        context['owner_profile'] = getattr(request.user, 'ownerprofile', None)
    else:
        context['recent_bookings'] = request.user.bookings.all()[:5]
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def owner_register(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Only owners can access this page.')
        return redirect('dashboard')
    
    if hasattr(request.user, 'ownerprofile'):
        messages.info(request, 'You have already submitted your verification documents.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                owner_profile = form.save(commit=False)
                owner_profile.user = request.user
                owner_profile.save()
                messages.success(request, 'Verification documents submitted successfully!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error saving profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OwnerRegistrationForm()
    
    return render(request, 'accounts/owner_register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    # Prepare context data for template
    context = {}
    
    if request.user.user_type == 'user':
        context['total_bookings'] = request.user.bookings.count()
        context['active_bookings'] = request.user.bookings.filter(status='confirmed').count()
        context['has_bookings'] = request.user.bookings.exists()
    elif request.user.user_type == 'owner':
        context['total_properties'] = request.user.properties.count()
        context['total_rooms'] = 0
        for property_obj in request.user.properties.all():
            context['total_rooms'] += property_obj.rooms.count()
    
    return render(request, 'accounts/profile.html', context)

@login_required
def verify_owner(request, owner_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Only admins can verify owners.')
        return redirect('dashboard')
    
    owner_profile = get_object_or_404(OwnerProfile, id=owner_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            owner_profile.verification_status = 'approved'
            owner_profile.save()  # This will trigger the save method in OwnerProfile model
            messages.success(request, f'Owner {owner_profile.user.username} has been verified.')
        elif action == 'reject':
            owner_profile.verification_status = 'rejected'
            owner_profile.save()  # This will trigger the save method in OwnerProfile model
            messages.warning(request, f'Owner {owner_profile.user.username} has been rejected.')
    
    return redirect('dashboard')


