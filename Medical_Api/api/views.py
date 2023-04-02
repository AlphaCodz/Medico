from django.shortcuts import render
from django.http import JsonResponse
from helpers.views import BaseView
from .models import PrimaryUser, Appointment, MedicalData
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import Jsonify_user
from .permissions import IsPatient
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.utils import timezone

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
        patient = PrimaryUser(email=request.data["email"])
        patient.first_name = request.data["first_name"]
        patient.last_name = request.data["last_name"]
        patient.set_password(raw_password=request.data["password"])
        patient.is_patient = True
        patient.is_medic = False
        patient.save()
        
        resp = {
            "code":201,
            "message":"Congratulations! Registered Successfully" 
                }
        return Response(resp, 201)
        
        
class DoctorReg(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "password"]  
    def post(self, request, format=None):
        super().post(request, format)
        def post(self, request, format=None):
            if PrimaryUser.objects.filter(email=request.data["email"]).exists():
                resp = {
                    "code":400,
                    "message": "Sorry email is taken"
                }
                return Response(resp, 400)
        doc = PrimaryUser(email=request.data["email"])
        doc.first_name = request.data["first_name"]
        doc.last_name = request.data["last_name"]
        doc.email = request.data["email"]
        doc.set_password(raw_password=request.data["password"])
        doc.is_patient = False
        doc.is_medic = True
        doc.save()
        resp = {
            "code":201,
            "message":"Congratulations! Registered Successfully" 
            }
        return Response(resp, 201)
    
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
            return Response(resp)
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
            resp = {
                "code": 200,
                "message": "SuccessFul",
                "doctors": Jsonify_user(doctor)
            }
            doc_list.append(resp)
            context_data = {"doctors":doc_list}
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
        # Get User
        if not this_user:
            return {
                "code": 404,
                "message": "User Not Found"
            }
        appointment = Appointment(user=this_user)
        schedule_date_str = request.data.get("schedule_date")
        appointment.schedule_date = timezone.make_aware(datetime.strptime(schedule_date_str, f'%Y-%m-%d %H:%M:%S'))
        appointment.referral_letter = request.data.get("referral_letter")
        appointment.medical_issue = request.data.get("medical_issue")
        appointment.save()
        resp = {
            "code":201,
            "user": Jsonify_user(this_user),
            "message": "Appointment Created Succesfully",
            "appointment date": str(appointment.schedule_date),
            "refferal letter": str(appointment.referral_letter),
            "medical issues": appointment.medical_issue
        }
        return Response(resp, 201)
    
class AppointmentList(APIView):
    permission_classes = [IsPatient,]
    def get(self, request, format=None):
        user = request.user
        appointments = Appointment.objects.filter(user=user)
        li = []
       
        for appointment in appointments:
           resp = {
                "first name": appointment.user.first_name,
                "last name": appointment.user.last_name,
                "medical issue": appointment.medical_issue,
                "referral letter": appointment.referral_letter if appointment.referral_letter else None,
                "schedule date": appointment.schedule_date.date(),
                "schedule time": appointment.schedule_date.time()
                  }
           li.append(resp)
           app_data = {"appoinments":li}
        return JsonResponse(app_data)
       
        

          
      
      

        
        
        
        
        
       
        
        

    
        
        
        
        
        
        
        
        
    
    
        