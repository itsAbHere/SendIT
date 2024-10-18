from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.conf import settings



class User(AbstractUser):
    
    class meta:
        app_label = 'Sendit'
    pass
    class Meta:
        # Add this Meta class to prevent clashes with auth.User
        swappable = 'AUTH_USER_MODEL'

    # Specify unique related names for the relationships
    groups = models.ManyToManyField(Group, related_name='sendit_users_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='sendit_users_permissions'
    )

class File(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='save/')

class FilePermission(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# Create your models here.
