from django.contrib import admin
from users_register_app.models import UserProfileInfo
# Register your models here.
# Report to admin site that we want to register our models
# If we don't register, we are not going to see changes in our admin site.
admin.site.register(UserProfileInfo)
