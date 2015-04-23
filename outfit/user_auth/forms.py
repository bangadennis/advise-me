from django import forms
from django.contrib.auth.models import User
from user_auth.models import UserDetails, ClothDescription, UserActivity, ClothFactBase
from crispy_forms.helper import FormHelper
#from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

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
    dateofbirth = forms.DateField(label="Date Of Birth ",
        widget=DateWidget(usel10n=True, bootstrap_version=3), required=True
        )
    occupation=forms.CharField(label="Occupation", required=True,)
    residence=forms.CharField(label="Place of Residence",
                              widget=forms.TextInput(
                                attrs={'id': 'autocomplete', 'onFocus':'geolocate()'}))
    class Meta:
        model=UserDetails
        fields=('gender','dateofbirth' , 'occupation','residence', 'profile_picture',)
        
#ttrs={'id': 'uploadImage', 'onchange':'PreviewImage()'
#Cloths Description Form 
class ClothDescriptionForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    cloth_description=forms.CharField(label="Cloth Description", required=True,)
    
    class Meta:
        model=ClothDescription
        fields=('cloth_image', 'cloth_description',)
        

#UserActivity Form 
class UserActivityForm(forms.ModelForm):
    
    category_choices=(('',''),('Job Interview', 'Job Interview'),('Business Formal', 'Business Formal'),
        ('Business Casual', 'Business Casual'),('Cocktail', 'Cocktail'),
        ('Date', 'Date'),('Religious', 'Religious'),('Funeral', 'Funeral'),('Wedding', 'Wedding'),
        ('School Event', 'School Event'),('Shopping', 'Shopping/Casual'),('Black Tie','Black Tie'),
        ('White Tie','White Tie'))
    helper = FormHelper()
    helper.form_tag = False
    
    event_location=forms.CharField(widget=forms.TextInput(attrs={'id': 'autocomplete', 'onFocus':'geolocate()'}))
    
    event_date= forms.DateField(label="Date of Event",
        widget=DateWidget(usel10n=True, bootstrap_version=3), required=True,
        )
    start_time= forms.TimeField(label="Start Time",
        widget=TimeWidget(usel10n=True, bootstrap_version=3), required=True,
        )
    
    category=forms.ChoiceField(widget=forms.Select(), choices=category_choices,
                               label="Category/Dress Codes",)
    class Meta:
        model=UserActivity
        exclude=('user',)
    
#ClothFactbase Form
class ClothFactForm(forms.ModelForm):
    
    #Cloth Types Choices
    
    
    #choice male
    choices_male=(('',''),('Shirt', 'Shirt'), ('T-Shirt', 'T-Shirt'),('Polo Shirt', 'Polo Shirt'),
        ('Dressy Shirt','Dressy Shirt'),('Full Suit', 'Full Suit'),
        ('Trouser', 'Trouser'),('Short', 'Short'),
        ('Khakis','Khakis'), ('Turtleneck','Turtleneck'),('Jacket', 'Jacket'), ('Cardigan', 'Cardigan'),
        ('Sportcoat','Sportcoat'), ('Blazer','Blazer'), ('Waistcoat','Waistcoat'),
        ('Tailcoat', 'Tailcoat'),
        ('Rain Coat','Rain Coat'),('Scarf','Scarf'),('Hat', 'Hat'),("Bow Tie","Bow Tie"),
        ('Trench Coat', 'Trench Coat'),("Gloves","Gloves"),
        )
    
    
    #choice female
    choices_female=(('',''), ('Dress', 'Dress'),('Pants', 'Pants'), ('Sweater', 'Sweater'),
        ('Shirt', 'Shirt'),('Short Skirt', 'Short Skirt'), ('Mid-Length Skirt', 'Mid-Length Skirt'),
        ('Long Skirt', 'Long Skirt'),
        ('Jacket', 'Jacket'),('Full Suit', 'Full Suit'),('Top', 'Top'),('Blouse', 'Blouse'),
        ("Turtleneck", "Turtleneck"),
        ('Mid-Length Dress', 'Mid-Length Dress'),('Long Dress', 'Long Dress'),
        ('Short Dress', 'Short Dress'),('Maxi Dress', 'Maxi Dress'),
        ('Blazer', 'Blazer'),('Suit Jacket', 'Suit Jacket'), ('Cardigan', 'Cardigan'),
        ('Jeans', 'Jeans'),('Khakis','Khakis'),('Short','Short'),('Gloves', 'Gloves'),
        ('Brim Hat', 'Brim Hat'),('Rain Coat','Rain Coat'),
        ('Scarf','Scarf'), ('Trench Coat', 'Trench Coat'), )
    choices_type=()
    #Color Choices
    choices_color=(('',''),('Red', 'Red'), ('Blue', 'Blue'), ('Black', 'Black'),
        ('White', 'White'),('Gray', 'Gray'),('Navy', 'Navy'),('Green', 'Green'), ('Pink', 'Pink'),
        ('Purple','Purple'),('Brown','Brown'), ('Peach', 'Peach'),('Royal Blue', 'Royal Blue'),
        ('Light Blue', 'Light Blue'),('Yellow', 'Yellow'),('Multi-Color','Multi-Color'))
    
    #Material Choices
    choices_material=(('',''),('Cotton', 'Cotton'), ('Silk', 'Silk'), ('Wool', 'Wool'), ('Nylon', 'Nylon'),
        ('Polyester', 'Polyester'), ('Denim', 'Denim'), ('Knitwear', 'Knitwear'), ('Lace','Lace' ),
        ('Chiffon', 'Chiffon'), ('Cashmere', 'Cashmere'), ('Spandex', 'Spandex'),('Leather', 'Leather'))
    #Cloth Print Choices
    choices_print=(('',''), ('Plain', 'Plain'),('Striped', 'Striped'), ('Floral', 'Floral'), ('Geometric', 'Geometric'),
        ('checked','checked'),)
    
    helper = FormHelper()
    helper.form_tag =False
    cloth_type=forms.ChoiceField(widget=forms.Select(), choices=choices_type,
                                 label="Select Type of Cloth",)
    cloth_color=forms.ChoiceField(widget=forms.Select(), choices=choices_color,
                                  label="Select The Color of the Cloth",)
    cloth_material=forms.ChoiceField(widget=forms.Select(), choices=choices_material,
                                     label="Select Material/Fabric of Cloth",)
    cloth_print=forms.ChoiceField(widget=forms.Select(), choices=choices_print,
                                  label="Select The Print of the Cloth",)

    class Meta:
        model=ClothFactBase
        exclude=('cloth',)
    #constructor
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ClothFactForm, self).__init__(*args, **kwargs)
        if self.user.gender=="Female":
            self.fields['cloth_type'].choices=self.choices_female
        else:
            self.fields['cloth_type'].choices=self.choices_male
            
        
        
        