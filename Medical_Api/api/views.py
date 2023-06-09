from django.shortcuts import render
from django.http import JsonResponse
from helpers.views import BaseView
from .models import PrimaryUser, Appointment, MedicalData, Document
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import Jsonify_user, Jsonify_doc
from .permissions import IsPatient,IsMedic
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db.models import Prefetch
from django.db.models import Q
from rest_framework import permissions
from django.core.paginator import Paginator
from .models import DiagnosisForm, CardGenerator
# Create your views here.
class PatientReg(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "password"]
    def post(self, request, format=None):
        super().post(request, format)
        if PrimaryUser.objects.filter(email=request.data["email"]).exists():
            resp = {
                "code":400,
                "message": "Sorry email is taken"
            }
            return Response(resp, 400)
        patient = PrimaryUser.objects.create(
            email = request.data["email"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            is_patient=True,
            is_medic=False
        )
        patient.set_password(raw_password=request.data["password"])
        patient.save()
        resp = {
            "code":201,
            "message":"Congratulations! Registered Successfully",
            "status": patient.is_patient
                }
        return Response(resp, 201)
        
        
class DoctorReg(BaseView):
    required_post_fields = ["first_name", "last_name", "specialty", "profile_image", "years_of_experience", "other", "email", "password"]  
    def post(self, request, format=None):
        super().post(request, format)
        def post(self, request, format=None):
            if PrimaryUser.objects.filter(email=request.data.get("email")).exists():
                resp = {
                    "code":400,
                    "message": "Sorry email is taken"
                }
                return Response(resp, 400)
        doc = PrimaryUser(email=request.data["email"])
        doc.first_name = request.data["first_name"]
        doc.last_name = request.data["last_name"]
        doc.specialty = request.data["specialty"]
        doc.years_of_experience = request.data["years_of_experience"]
        doc.profile_image = request.data["profile_image"]
        doc.set_password(raw_password=request.data["password"])
        doc.is_medic=True
        doc.is_patient=False
        
        # Check if specialty is not among the listed field
        if doc.specialty == "OTHER":
            doc.other = request.data["other"]
        else:
            doc.other = None
        doc.save()
        resp = {
            "code":201,
            "message":"Congratulations! Registered Successfully",
            "Doctor": {
                "data": Jsonify_doc(doc)
            }
            }
        return Response(resp, 201)

class AllUsers(BaseView):
    def get(self, request, format=None):
        users = PrimaryUser.objects.filter(is_patient=True)
        resp = {
            "code": 200,
            "patients": [Jsonify_user(user) for user in users]
        }
        return Response(resp, 200)
class AdminReg(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "staff_number","password"]
    def post(self, request):
        data = request.data
        if PrimaryUser.objects.filter(email=data["email"]).exists():
            resp = {
                "code":400,
                "message": "Sorry Email is Taken"
            }
            return Response(resp, 400)
        if PrimaryUser.objects.filter(staff_number=data["staff_number"]).exists():
            resp = {
                "code":400,
                "message": "Sorry Staffs can't have double accounts"
            }
            return Response(resp,400)
        
        admin = PrimaryUser.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            staff_number=data["staff_number"],
        )
        admin.set_password(raw_password=data["password"])
        admin.is_admin=True
        admin.is_medic=False
        admin.is_patient=True
        admin.save()
        data = {
            "code": 201,
            "data":Jsonify_user(admin) 
        }
        return Response(data, 201)
    

class Notification(APIView):
    def get(self, request, format=None):
        user = request.user
        two_hrs_ago = datetime.now() - timedelta(hours=2)
        
        # Get New Users
        new_users = PrimaryUser.objects.filter(is_patient=True, created_at__gte=two_hrs_ago)
        
        # Get New Doctors
        new_docs = PrimaryUser.objects.filter(is_medic=True, created_at__gte=two_hrs_ago)
        
        user_data = [{"first_name": new_user.first_name, "last_name": new_user.last_name} for new_user in new_users]
        
        doc_data= [{"first_name": new_doc.first_name, "last_name": new_doc.last_name} for new_doc in new_docs]
        
        context = {
            "new_users": user_data,
            "new_docs": doc_data
        }
        return Response(context, 200)
   
class AdminData(BaseView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        admin_data = Jsonify_user(request.user)
        res = {
            "code": 200,
            "message": "success",
            "admin": admin_data
        }
        return Response(res)
    
class Login(BaseView):
    required_post_fields = ["email", "password"]
    def post(self, request, format=None):
        super().post(request, format)
        
        # Check if user exists
        user = PrimaryUser.objects.filter(email=request.data["email"]).first()
        if not user:
            resp = {
                "code": 404,
                "message": "Incorrect Email please try again!"
            }
            return Response(resp, 404)
        if user.check_password(raw_password=request.data["password"]):
            token = RefreshToken.for_user(user)
            print(token)
            resp = {
                "code":200,
                "message": "Login Successful",
                "user_data": Jsonify_user(user),
                "token": str(token.access_token)   
            }
            return Response(resp, 200)
        resp = {
            "code":401,
            "message": "Incorrect Password"
        }
        return Response(resp, 401)
       

class LogoutView(APIView):
    permission_classes = (IsAuthenticated)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class AllDoctors(APIView):
    # permission_classes = [IsAuthenticated,]
    def get(self, request, *args, **kwargs):
        # PAGINATE
        doctors = PrimaryUser.objects.filter(is_medic=True).order_by("id")
        # paginator = Paginator(doctors, 7)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        
        doc_list = []
        for doctor in doctors:
            doc_list.append(Jsonify_doc(doctor))
        context_data = {
            "code": 200,
            "message": "SuccessFul",
            "doctors": doc_list
        }
        return JsonResponse(context_data)
    
class AddMedData(BaseView):
    required_post_fields = ["race", "occupation", "blood_group", "medical_cases", "home_address"]
    permission_classes = [IsPatient, ]
    def post(self, request, format=None):
        # print(request.headers)
        user = request.user
        medical_data = MedicalData(user=user)
        medical_data.race = request.data["race"]
        medical_data.occupation = request.data["occupation"]
        medical_data.blood_group = request.data["blood_group"]
        medical_data.medical_cases = request.data["medical_cases"]
        medical_data.home_address = request.data["home_address"]
        medical_data.is_submitted=True
        medical_data.save()
        resp = {
            "code":201,
            "messsage": "Medical Data Added Successfully",
            "medical_data": {
                "patient": Jsonify_user(user),
                "race": medical_data.race,
                "occupation": medical_data.occupation,
                "blood_group": medical_data.blood_group,
                "medical_cases": medical_data.medical_cases,
                "home_address": medical_data.home_address
            },
            "medical status check": {
                "has_submitted": medical_data.is_submitted
            }
        }
        return Response(resp, 201)
    
    
class MedStatus(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, *args, **kwargs):
        user = request.user
        status = MedicalData.objects.filter(user=user).first()
        if status and status.is_submitted:
            resp = {
                "code": 200,
                "status": True
            }
            return Response(resp, 200)
        else:
            resp = {
                "code": 200,
                "status": False
            }
            return Response(resp, 200)   
        
            
class CreateAppointment(APIView):
    permission_classes = [IsPatient,]

    def post(self, request, medic_id):
        this_user = request.user
        medic = PrimaryUser.objects.filter(is_medic=True, id=medic_id).first()
        medic_id = medic.id if medic else None

        # Get User
        if not this_user:
            return Response({
                "code": 404,
                "message": "User Not Found"
            }, status=404)

        appointment = Appointment(user=this_user)

        schedule_date_str = request.data.get("schedule_date")
        if schedule_date_str:
            try:
                appointment.schedule_date = timezone.make_aware(datetime.strptime(schedule_date_str, '%Y-%m-%d %H:%M:%S'))
            except ValueError:
                return Response({
                    "code": 400,
                    "message": "Invalid schedule date format, should be: 'YYYY-MM-DD HH:MM:SS'"
                }, status=400)

        appointment.referral_letter = request.data.get("referral_letter")
        appointment.medical_issue = request.data.get("medical_issue")

        if medic_id:
            appointment.medic_id = medic_id
            
        appointment.save()
        resp = {
            "code": 201,
            "user": Jsonify_user(this_user),
            "message": "Appointment Created Successfully",
            "appointment_date": str(appointment.schedule_date),
            "referral_letter": str(appointment.referral_letter),
            "medical_issues": appointment.medical_issue,
            "assigned_to": f"{appointment.medic.first_name} {appointment.medic.last_name}" if appointment.medic else None
        }

        return Response(resp, status=201)

    
class AppointmentList(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, format=None):
        user = request.user
        appointments = Appointment.objects.filter(user=user)
        doctors = PrimaryUser.objects.filter(is_medic=True, appointment__in=appointments)
        data_list = []
       
        for appointment in appointments:
            resp = {
                "first_name": appointment.user.first_name,
                "last_name": appointment.user.last_name,
                "appointments": []
            }
            for appointment in appointments.filter(user=appointment.user):
                res = {
                    "schedule_date": appointment.schedule_date.date(),
                    "schedule_time": appointment.schedule_date.time(),
                }
                for doctor in doctors:
                    if appointment.user == doctor:
                        doc_res = {
                            "doctor": f"Dr. {doctor.first_name} {doctor.last_name}"
                        }
                        res.update(doc_res)
                resp["appointments"].append(res)
            data_list.append(resp)
        return Response(data_list)   
    
    from django.utils import timezone


                        
class GetMyAppointment(BaseView):
    permission_classes = [IsMedic,]
    def get(self, request, format=None):
        user_id = request.user.id
        # current_time = timezone.now()
        appointments = Appointment.objects.filter(medic=user_id)
        data = [{"id":appointment.id, "first_name":appointment.user.first_name, "last_name": appointment.user.last_name, 
            "medical_case": appointment.medical_issue, "schedule_date": str(appointment.schedule_date.date()), 
            "schedule_time": str(appointment.schedule_date.time())} for appointment in appointments]
        resp = {
            "code": 200,
            "data": data
        }
        return Response(resp, 200)

class Assigned(BaseView):
    def get(request, format=None):
        assigned_appointments = Appointment.objects.filter(medic__isnull=False)
        assigned_patients = [{"id": appointment.user.id, "first_name": appointment.user.first_name, "last_name": appointment.user.last_name, "medical_cases":appointment.medical_issue} for appointment in assigned_appointments]
        resp = {
            "code": 200,
            "data": assigned_patients
        }
        return Response(resp, status =200)
        

class CreateDocument(BaseView):
    permission_classes = [IsAuthenticated,]
    required_post_fields = ["title", "description", "file"]
    def post(self, request, format=None):
        document = Document.objects.create(
            user=request.user,
            title=request.data["title"],
            description=request.data["description"],
            file=request.data["file"]
        )
        document.save()
        resp = {
            "code": 201,
            "message": "Documents Created Successfully"
        }
        return Response(resp, 201)
      
      
class CreateDiagForm(BaseView):
    required_post_fields=["patient", "diagnosis", "submitted_at", "prescription", "additional_notes"]
    def post(self, request, patient_id):
        try:
            patient = PrimaryUser.objects.get(id=patient_id)
        except PrimaryUser.DoesNotExist:
            resp = {
                "code": 404,
                "message": "Patient Not Found"
            }
            return Response(resp, 404)
        diagnosis = DiagnosisForm(
            patient=patient,
            diagnosis=request.POST["diagnosis"],
            prescription=request.POST["prescription"],
            additional_notes= request.POST["additional_notes"]
            
        )
        diagnosis.save()
        resp = {
            "code":201,
            "message": "Successful"
        }
        return Response(resp, 201)
    
class MyDiag(APIView):
    def get(self, request, format=None):
        user=request.user.id
        try:
            diags = DiagnosisForm.objects.filter(patient=user)
        except DiagnosisForm.DoesNotExist:
            return Response({
                "code": 404,
                "message": "No Diagnosis Yet"
            }, 404)
        data = [{"diagnosis": diag.diagnosis, "date_submitted": diag.submitted_at.date(), "time_submitted":diag.submitted_at.time(), 
                 "prescription": diag.prescription, "additional_notes":diag.additional_notes} 
                    for diag in diags]
        resp = {
            "code": 200,
            "data": data
        }
        return Response(resp, 200)
    
class GenerateHospitalCard(BaseView):
    required_post_fields = ["patient", "medical_record", "hospital_branch"]
    def post(self, request, patient_id):
        try:
            patient = PrimaryUser.objects.get(id=patient_id)
        except PrimaryUser.DoesNotExist:
            resp = {
                "code": 404,
                "message": "User Does Not Exist"
            }
            return Response(resp, 404)
        
        try:
            medical_record = MedicalData.objects.get(user=patient_id)
        except MedicalData.DoesNotExist:
            resp = {
                "code": 404,
                "message": "Medical Data Does Not Exist"
            }
            return Response(resp, 404)
        
        card = CardGenerator.objects.create(
            patient=patient,
            medical_record=medical_record,
            hospital_branch=request.POST["hospital_branch"]
        )
        card.save()
        resp = {
            "code": 201,
            "message": "Created Successfully",
            "data": {
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "blood_group": card.medical_record.blood_group,
                "medical_cases": card.medical_record.medical_cases,
                "hospital_branch": card.hospital_branch
            }
        }
        return Response(resp, 201)
    
class MyCard(APIView):
    permission_classes = [IsPatient,]
    def get(self, request, format=None):
        patient = request.user.id
        try:
            card = CardGenerator.objects.get(patient=patient)
        except CardGenerator.DoesNotExist:
            resp = {
                "code": 404,
                "message": "Patient Does Not Exist"
            }
        try:
            medical_data = MedicalData.objects.get(user=patient)
        except MedicalData.DoesNotExist:
            resp = {
                "code": 404,
                "message": "Patient Record Doesn't Exist"
            }
        
        data = {
            "code":200,
            "first_name": card.patient.first_name,
            "last_name": card.patient.last_name,
            "medical_record": {
                "blood_group": card.medical_record.blood_group,
                "medical_cases": card.medical_record.medical_cases,
                "hospital_branch": card.hospital_branch
            }
        }
        return Response(data, 200)
        
        
        
        

    
        
        
        
        
        
        
        
        
    
    
        