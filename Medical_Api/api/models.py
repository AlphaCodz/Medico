from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class PrimaryUser(User):
    is_patient = models.BooleanField(default=False)
    is_medic = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name
    
    
class Appointment(models.Model):
    user = models.ForeignKey(PrimaryUser, on_delete=models.PROTECT)
    schedule_date = models.DateField(null=True)
    schedule_time  = models.TimeField(null=True)
    # referral_letter = models.FileField()
    
    def __str__(self):
        return self.user.first_name
    
    
    
    
    
# - Register for patients (post)
# - Register for doctors (post)
# - Login (post)
# - get lost of doctors (Get)
# - to submit appointment form (post)