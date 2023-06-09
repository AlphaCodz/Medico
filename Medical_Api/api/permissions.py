from .models import PrimaryUser
from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        patient = PrimaryUser.objects.filter(is_patient=True).exists()
        return patient
    
class IsMedic(BasePermission):
    def has_permission(self, request, view):
        medic = PrimaryUser.objects.filter(is_admin=True).exists()
        return medic