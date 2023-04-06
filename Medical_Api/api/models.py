from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
import random as rand
from cloudinary_storage.storage import RawMediaCloudinaryStorage
import os
from django.conf import settings


# Create your models here.
class PrimaryUser(AbstractBaseUser):
    SPECIALTY = (
        ("PEDIATRICIAN", "PEDIATRICIAN"),
        ("NEUROLOGIST", "NEUROLOGIST"),
        ("GYNECOLOGIST", "GYNECOLOGIST"),
        ("PHYSIOTHERAPIST", "PHYSIOTHERAPIST"),
        ("ONCOLOGIST", "ONCOLOGIST"),
        ("CARDIOLOGIST", "CARDIOLOGIST"),
        ("OPHTHAMOLOGIST", "OPHTHAMOLOGIST"),
        ("PSYCHIATRIST", "PSYCHIATRIST"),
        ("DERMALOGIST", "DERMATOLOGIST"),
        ("OTHER", "OTHER")
    )
    
    
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=10, unique=True, null=True)
    specialty = models.CharField(choices=SPECIALTY, max_length=30, null=True)
    years_of_experience = models.CharField(max_length=10, null=True)
    other= models.CharField(max_length=30, null=True)
    is_patient = models.BooleanField(default=False)
    profile_image = models.FileField(storage=RawMediaCloudinaryStorage(), null=True)
    is_medic = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    
    def __str__(self):
        return self.first_name
    
    def get_file_url(self):
        if self.profile_image:
            filename = os.path.basename(self.profile_image.name)
            return f"{settings.CLOUDINARY_STORAGE['CLOUDINARY_URL']}/{filename}"
        else:
            return None
    
    def save(self, *args, **kwargs):
        code = rand.randint(11000, 99999)
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