from django import forms
from django.contrib.auth.models import User
from user_auth.models import UserProfile
from bootstrap3_datetime.widgets import DateTimePicker

#UserForm
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','first_name','last_name', 'email', 'password')
        

#UserProfileForm
class UserProfileForm(forms.ModelForm):
     dateofbirth=forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                "pickTime": False}))
     class Meta:
        model=UserProfile
        fields=('dateofbirth', 'skincolor', 'occupation')
    
    