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
    RACE = (
        ("BLACK", "BLACK"),
        ("WHITE", "WHITE"),
        ("COLORED", "COLORED"),
        ("OTHER", "OTHER")
    )
    
    OCCUPATION = (
        ("VENDOR", "VENDOR"),
        ("BUSINESS OWNER", "BUSINESS OWNER"),
        ("CIVIL SERVANT", "CIVIL SERVANT"),
        ("EDUCATOR", "EDUCATOR"),
        ("DRIVER", "DRIVER"),
        ("CONSTRUCTION WORKER", "CONSTRUCTION WORKER"),
        ("LABOURER", "LABOURER"),
        ("STUDENT/PUPIL", "STUDENT/PUPIL"),
        ("GENERAL ASSISTANT", "GENERAL ASSISTANT"),
        ("OTHER", "OTHER")      
    )
    
    BLOOD_GROUP = (
        ("O+", "O+"),
        ("O-", "O-"),
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-") 
    )
    
    user = models.OneToOneField(PrimaryUser, on_delete=models.CASCADE)
    race = models.CharField(choices=RACE, max_length=7)
    occupation = models.CharField(choices=OCCUPATION, max_length=25)
    blood_group = models.CharField(choices=BLOOD_GROUP, max_length=4)
    medical_cases = models.TextField()
    home_address = models.CharField(max_length=300, null=True)
    is_submitted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name
    
    

        
        
    
    
class Appointment(models.Model):
    user = models.ForeignKey(PrimaryUser, on_delete=models.PROTECT, null=True)
    schedule_date = models.DateTimeField(null=True)
    referral_letter = models.FileField(upload_to="ref_letters/", null=True)
    medical_issue = models.TextField(null=True)
    
    def __str__(self):
        return self.user.first_name
    
    def get_user():
        users = PrimaryUser.objects.filter(is_medic=True)
        
        
# - Register for patients (post)
# - Register for doctors (post)
# - Login (post)
# - get lost of doctors (Get)
# - to submit appointment form (post)