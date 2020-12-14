from django.contrib import admin
from .models import Cheese

# Add Cheeses section in Admin page
admin.site.register(Cheese)
