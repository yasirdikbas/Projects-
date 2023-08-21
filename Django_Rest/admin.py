from django.contrib import admin
from django.apps import apps

from .models import *


# Registering our models to view them in Admin Panel 
admin.site.register(test_list)
admin.site.register(test_case)
admin.site.register(known_error)