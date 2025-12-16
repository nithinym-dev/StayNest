from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Min
from django.db import transaction
from .models import Property, Room, PropertyImage
from .forms import PropertyForm, RoomForm, PropertyImageForm

def property_list(request):
    properties = Property.objects.filter(is_active=True).annotate(
        min_price=Min('rooms__daily_rate')
    )
    
    # Search and filter logic
    search = request.GET.get('search')
    city = request.GET.get('city')
    property_type = request.GET.get('property_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if search:
        properties = properties.filter(
            Q(name__icontains=search) | 
            Q(address__icontains=search) |
            Q(city__icontains=search)
        )
    
    if city:
        properties = properties.filter(city__icontains=city)
    
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    if min_price:
        properties = properties.filter(rooms__daily_rate__gte=min_price).distinct()
    
    if max_price:
        properties = properties.filter(rooms__daily_rate__lte=max_price).distinct()
    
    # Get unique cities for filter dropdown
    cities = Property.objects.values_list('city', flat=True).distinct()
    
    context = {
        'properties': properties,
        'cities': cities,
        'search': search,
        'selected_city': city,
        'selected_type': property_type,
        'min_price': min_price,
        'max_price': max_price,
    }
    
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    rooms = property_obj.rooms.all()  # Show all rooms to owner
    
    context = {
        'property': property_obj,
        'rooms': rooms,
    }
    
    return render(request, 'properties/property_detail.html', context)

@login_required
def add_property(request):
    if request.user.user_type != 'owner' or not request.user.is_verified:
        messages.error(request, 'Only verified owners can add properties.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save property
                    property_obj = form.save(commit=False)
                    property_obj.owner = request.user
                    property_obj.save()

                    # Handle image uploads
                    images = request.FILES.getlist('images')
                    for i, image in enumerate(images):
                        PropertyImage.objects.create(
                            property_obj=property_obj,
                            image=image,
                            is_primary=(i == 0)  # First image is primary
                        )

                messages.success(request, 'Property added successfully!')
                return redirect('add_room', property_id=property_obj.id)
            except Exception as e:
                messages.error(request, f'Error saving property: {str(e)}')
                return render(request, 'properties/add_property.html', {'form': form})
    else:
        form = PropertyForm()
    
    return render(request, 'properties/add_property.html', {'form': form})

@login_required
def add_room(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, owner=request.user)
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            try:
                room = form.save(commit=False)
                room.property_obj = property_obj
                room.save()
                messages.success(request, 'Room added successfully!')
                return redirect('property_detail', pk=property_obj.pk)
            except Exception as e:
                messages.error(request, f'Error saving room: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoomForm()
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'properties/add_room.html', context)

@login_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk, property_obj__owner=request.user)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Room updated successfully!')
                return redirect('property_detail', pk=room.property_obj.pk)
            except Exception as e:
                messages.error(request, f'Error updating room: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoomForm(instance=room)
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'properties/edit_room.html', context)
