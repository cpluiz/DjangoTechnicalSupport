from django.db import models
from django.contrib.auth.models import AbstractUser

# User contains Admin or Attendant
class User(AbstractUser):
    pass
