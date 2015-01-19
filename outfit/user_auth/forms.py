from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

#UserForm
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username', 'email', 'password')
        
        

#UserProfileForm
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model=UserForm
        fields=('dateofbirth', 'skincolor', 'occupation')
    
    