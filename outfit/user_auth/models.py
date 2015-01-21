from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# UserProfile model
class UserDetails(models.Model):
    user=models.OneToOneField(User)
    #additional details
    dateofbirth=models.DateField(blank=False, null=False)
    skintone=models.CharField(max_length=30,blank=False, null=False)
    occupation=models.CharField(max_length=30,blank=False, null=False)
    profile_picture= ProcessedImageField(upload_to='images/profileImages',blank=True,
                                           processors=[ResizeToFill(100, 50)],
                                           format='JPEG',
                                           options={'quality': 60})
    
    def __unicode__(self):
        return self.user.username
    
class ClothDescription(models.Model):
    user=models.ForeignKey(User)
    cloth_image=ProcessedImageField(upload_to='images/wadrobe',blank=False,
                                           processors=[ResizeToFill(300, 300)],
                                           format='JPEG',
                                           options={'quality': 60})

    cloth_description=models.TextField(blank=False, null=False)
    
    def __unicode__(self):
        return self.user.username
    
#class UserActivity(models.Model):
   # activity_id=models.AutoField(primary_key=True)
   # user=models.ForeignKey(User)
   # category=models.CharField(max_length=40, blank=False, null=False)
   # event_name=models.CharField(max_length=30, blank=False, null=False)
   # event_date=models.DateField(blank=False, null=False)
    #start_time=models.TimeField(blank=False, null=False)
    #end_time=models.TimeField(blank=False, null=False)
    
    
