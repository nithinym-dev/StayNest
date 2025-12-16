from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, OwnerProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    user_type = forms.ChoiceField(choices=[('user', 'User'), ('owner', 'Owner')])
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'user_type', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

class OwnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['document_type', 'document_number', 'document_image', 'business_name', 'business_address']
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 3}),
        }
