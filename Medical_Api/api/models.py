from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
import random as rand


# Create your models here.
class PrimaryUser(AbstractBaseUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    is_patient = models.BooleanField(default=False, null=True)
    is_medic = models.BooleanField(default=False, null=True)
    username = models.CharField(max_length=10, unique=True, null=True)
    
    USERNAME_FIELD = "email"
    
    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        # Check if a user with the same username already exists
        if PrimaryUser.objects.filter(username=self.username).exists():
            raise ValueError('Username already exists')
        else:
            code = rand.randint(10000, 99999)
            self.username = code
        super().save(*args, **kwargs)
        

class MedicalData(models.Model):
    pass

        
        
    
    
class Appointment(models.Model):
    user = models.ForeignKey(PrimaryUser, on_delete=models.PROTECT)
    schedule_date = models.DateTimeField(null=True)
    # referral_letter = models.FileField()
    
    def __str__(self):
        return self.user.first_name
    
# - Register for patients (post)
# - Register for doctors (post)
# - Login (post)
# - get lost of doctors (Get)
# - to submit appointment form (post)