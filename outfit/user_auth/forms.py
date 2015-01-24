from django import forms
from django.contrib.auth.models import User
from user_auth.models import UserDetails, ClothDescription, UserActivity, ClothFactBase
from crispy_forms.helper import FormHelper
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
#from bootstrap3_datetime.widgets import DateTimePicker

#UserForm
class UserForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    password=forms.CharField(widget=forms.PasswordInput())
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=('first_name','last_name','username', 'email', 'password')
        

#UserProfileForm
class UserDetailsForm(forms.ModelForm):
    
    choices=(("Male","Male",),("Female","Female"),)
    helper = FormHelper()
    helper.form_tag = False
    gender=forms.ChoiceField(widget=forms.Select(),choices=choices, label="Gender", )
    dateofbirth = forms.DateField(label="Date Of Birh ",
        widget=BootstrapDateInput(), required=True,
        )
    skintone=forms.CharField(label="Skin Tone ", required=True,)
    occupation=forms.CharField(label="Occupation", required=True,)
    class Meta:
        model=UserDetails
        fields=('gender','dateofbirth', 'skintone', 'occupation', 'profile_picture',)
    
#Cloths Description Form and Q&A
class ClothDescriptionForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    cloth_description=forms.CharField(label="Cloth Description", required=True,)
    class Meta:
        model=ClothDescription
        fields=('cloth_image', 'cloth_description',)
        

#UserActivity Form 
class UserActivityForm(forms.ModelForm):
    category_choices=(('',''),('Wedding', 'Wedding'),('Funeral', 'Funeral'), ('Work', 'Work'), ('Party', 'Party'),)
    helper = FormHelper()
    helper.form_tag = False
    category=forms.ChoiceField(widget=forms.Select(), choices=category_choices, )
    class Meta:
        model=UserActivity
        exclude=('user',)
    
#ClothFactbase Form
class ClothFactForm(forms.ModelForm):
    choices_type=(('',''), ('topbottom', 'Dress'),('bottom', 'Pants'), ('top', 'Sweater'),
        ('top', 'Shirt'), ('top', 'Jacket'), ('bottom', 'Skirt'), ('flatshoes', 'FlatShoes'),
        ('highheelsshoes', 'HighHeels') )
    
    choices_color=(('',''),('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White'),
        ('multicolor', 'MultiColored'))
    
    choices_material=(('',''),('cotton', 'Cottom'), ('slik', 'Slik'), ('wool', 'Woolen'), ('nylon', 'Nylon'),
        ('polyester', 'Polyester'), ('denim', 'Denim'), ('knitwear', 'KnitWear'), ('lace','Lace' ),
        ('chifton', 'Chifton'), ('cashmene', 'Cashmene'), ('spandex', 'Spandex'))
    
    choices_print=(('',''),('striped', 'Stripped'), ('floral', 'Floral'), ('geometric', 'Geometric'), ('checked','Checked'))
    
    helper = FormHelper()
    helper.form_tag =False
    cloth_type=forms.ChoiceField(widget=forms.Select(), choices=choices_type, label="Select The Cloth Type",)
    cloth_color=forms.ChoiceField(widget=forms.Select(), choices=choices_color, label="Select The Color of the cloth",)
    cloth_material=forms.ChoiceField(widget=forms.Select(), choices=choices_material, label="Select The Cloth Material",)
    cloth_print=forms.ChoiceField(widget=forms.Select(), choices=choices_print, label="Select The Cloth Print",)

    class Meta:
        model=ClothFactBase
        exclude=('cloth_id',)
        
        
        