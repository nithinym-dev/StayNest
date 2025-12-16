from django import forms
from .models import Property, Room, PropertyImage  # This is correct - importing from the same app

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name', 'property_type', 'description', 'address', 'city', 'state', 'pincode',
            'latitude', 'longitude', 'wifi', 'meals', 'ac', 'laundry', 'parking', 'security'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'step': 'any'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_number', 'room_type', 'capacity', 'daily_rate', 'monthly_rate',
            'security_deposit', 'attached_bathroom', 'balcony'
        ]

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_primary']
