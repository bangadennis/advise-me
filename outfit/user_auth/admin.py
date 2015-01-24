from django.contrib import admin
from user_auth.models import UserDetails, ClothDescription, UserActivity, ClothFactBase

admin.site.register(UserDetails)
admin.site.register(ClothDescription)
admin.site.register(UserActivity)
admin.site.register(ClothFactBase)
# Register your models here.
