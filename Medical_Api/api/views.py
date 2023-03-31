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
        patient.email = request.data["email"]
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
    
class AddMedData(APIView):
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
        medical_data.save()
        resp = {
            "code":200,
            "messsage": "Medical Data Added Successfully",
            "medical_data": {
                "patient": Jsonify_user(user),
                "race": medical_data.race,
                "occupation": medical_data.occupation,
                "blood_group": medical_data.blood_group,
                "medical_cases": medical_data.medical_cases,
                "home_address": medical_data.home_address
            }
        }
        return Response(resp, 200)
        
                
        
                
        
# class CreateAppointment(APIView):
#     permission_classes = [IsPatient, ]
#     def post(self, request, medic_id): 
#         # CHECK MEDIC ID
#         try:
#             medic = PrimaryUser.objects.get(id=medic_id, is_medic=True)
#         except PrimaryUser.DoesNotExist:
#             return JsonResponse({'error': f'Medic with id {medic_id} does not exist or is not a medic.'}, status=400)
        
#         schedule_date = request.POST.get('schedule_date')
        
#         appointment = Appointment(user=user, assigned_medic=medic, schedule_date=schedule_date)
#         appointment.save()
#         return JsonResponse({'success': f'Appointment created for {request.first_name} {request.last_name} with {medic.first_name} {medic.last_name}.'}, status=201)
    
        
        
        
        
        
        
        
        
    
    
        