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
def Jsonify_doc(doc:PrimaryUser):
    return  {
        "first_name":doc.first_name,
        "last_name":doc.last_name,
        "email":doc.email,
        "username":doc.username,
        "profile image":doc.get_file_url(),
        "years of experience": doc.years_of_experience,
        "specialty":doc.specialty,
        "other": doc.other,
        "is_patient": doc.is_patient,
        "is_medic": doc.is_medic
    }