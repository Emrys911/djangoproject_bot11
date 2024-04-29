from django.db import models
from aiogram.types import User
class UserProfile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)