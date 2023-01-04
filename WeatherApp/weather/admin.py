from django.contrib import admin
from .models import User, UserFavourites

admin.site.register(User)
admin.site.register(UserFavourites)
