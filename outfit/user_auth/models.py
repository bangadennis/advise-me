from django.db import models
from django.contrib.auth.models import User

# UserProfile model
class UserProfile(models.Model):
    user=models.OneToOneField(User)
    #additional details
    dateofbirth=models.DateField(blank=False, null=False)
    skincolor=models.TextField(max_length=30,blank=False, null=False)
    occupation=models.TextField(max_length=30,blank=False, null=False)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    
    
    
