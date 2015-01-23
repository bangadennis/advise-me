from django.contrib import admin
from user_auth.models import UserDetails, ClothDescription, UserActivity

admin.site.register(UserDetails)
admin.site.register(ClothDescription)
admin.site.register(UserActivity)
# Register your models here.
