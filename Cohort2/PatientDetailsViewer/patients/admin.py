from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Patient
# Customize admin header
admin.site.site_header = "Online Hospital"
admin.site.site_title = "Online Hospital Admin Portal"
admin.site.index_title = "Welcome to Online Hospital Admin"


admin.site.register(Patient)