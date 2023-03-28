from .models import PrimaryUser

def Jsonify_user(user:PrimaryUser):
    return {
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
        "username":user.username,
        "is_patient": user.is_patient,
        "is_medic": user.is_medic
    }