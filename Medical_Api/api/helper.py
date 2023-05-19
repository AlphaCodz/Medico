from .models import PrimaryUser

def Jsonify_user(user:PrimaryUser):
    return {
        "id":user.id,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
        "username":user.username,
        "is_patient": user.is_patient,
        "is_medic": user.is_medic,
        "is_admin": user.is_admin
    }
def Jsonify_doc(doc:PrimaryUser):
    return  {
        "id": doc.id,
        "first_name":doc.first_name,
        "last_name":doc.last_name,
        "email":doc.email,
        "username":doc.username,
        "profile_image":doc.get_file_url(),
        "years_of_experience": doc.years_of_experience,
        "specialty":doc.specialty,
        "other": doc.other,
        "is_patient": doc.is_patient,
        "is_medic": doc.is_medic
    }

