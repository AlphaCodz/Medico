from django.shortcuts import render
from django.http import JsonResponse
from helpers.views import BaseView
from .models import PrimaryUser, Appointment, MedicalData
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import Jsonify_user, Jsonify_doc
from .permissions import IsPatient
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db.models import Prefetch
from django.db.models import Q
from rest_framework import permissions
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
        for user in users:
            resp = {
                "code": 200,
                "patients": Jsonify_user(user)
            }
            return Response(resp, 200)
        
class GetMyAppointment:
    def get(self, request, format=None):
        pass
    
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
    
class AdminData(BaseView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [IsAuthenticated,]
    def get(self, request, *args, **kwargs):
        doctors = PrimaryUser.objects.filter(is_medic=True)
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
    permission_classes = [IsPatient]

    def post(self, request):
        this_user = request.user
        medic = PrimaryUser.objects.filter(is_medic=True).first()
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
                        
                    
                       
               
           

        

          
      
      

        
        
        
        
        
       
        
        

    
        
        
        
        
        
        
        
        
    
    
        