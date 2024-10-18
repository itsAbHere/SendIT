# files/admin.py
from django.contrib import admin
from .models import User, File, FilePermission

admin.site.register(User)
admin.site.register(File)
admin.site.register(FilePermission)

