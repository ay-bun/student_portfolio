from django.contrib import admin

# Register your models here.
from user_profile.models import UserProfile, FacultyRole

admin.site.register(UserProfile)
admin.site.register(FacultyRole)