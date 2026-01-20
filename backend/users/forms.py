from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    """
    Extended registration form with user_type
    """
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        required=True,
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type']
            )
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    
    class Meta:
        model = UserProfile
        fields = ['phone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        # Update User model fields
        profile.user.username = self.cleaned_data['username']
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile
