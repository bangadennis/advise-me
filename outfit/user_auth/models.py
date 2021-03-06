from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# UserProfile model
class UserDetails(models.Model):
    user=models.OneToOneField(User)
    #additional details
    gender=models.CharField(max_length=10, blank=False, null=False, default="Male")
    dateofbirth=models.DateField(blank=False, null=False)
    occupation=models.CharField(max_length=50,blank=False, null=False)
    residence=models.CharField(max_length=50, blank=False, null=False,default="Nairobi, Kenya")
    profile_picture= ProcessedImageField(upload_to='images/profileImages',blank=True,
                                           processors=[ResizeToFill(100, 100)],
                                           format='JPEG',
                                           options={'quality': 100})
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('edit_userdetails', kwargs={'pk': self.pk})
    
    
class ClothDescription(models.Model):
    user=models.ForeignKey(User)
    cloth_image=ProcessedImageField(upload_to='images/wadrobe',blank=False,
                                           processors=[ResizeToFill(300, 300)],
                                           format='JPEG',
                                           options={'quality': 100})

    cloth_description=models.CharField(max_length=50, blank=False, null=False)
    
    def __unicode__(self):
        return self.user.username

    
class UserActivity(models.Model):
   activity_id=models.AutoField(primary_key=True)
   user=models.ForeignKey(User)
   category=models.CharField(max_length=50, blank=False, null=False)
   event_location=models.CharField(max_length=50, blank=False)
   event_name=models.CharField(max_length=50, blank=False, null=False)
   event_date=models.DateField(blank=False, null=False)
   start_time=models.TimeField(blank=False, null=False)
   
   def get_absolute_url(self):
        return reverse('edit_useractivity', kwargs={'pk': self.pk})

class ClothFactBase(models.Model):
    cloth=models.ForeignKey(ClothDescription)
    cloth_type=models.CharField(max_length=50, blank=False, null=False)
    cloth_color=models.CharField(max_length=50, blank=False, null=False)
    cloth_material=models.CharField(max_length=50, blank=False, null=False)
    cloth_print=models.CharField(max_length=50, blank=False, null=False)

    
    
    
    

   
    
    
