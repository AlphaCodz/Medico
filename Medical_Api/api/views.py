from django.shortcuts import render
from helpers.views import BaseView
from .models import PrimaryUser, Appointment
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import Jsonify_user

# Create your views here.
class PatientReg(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "password"]
    def post(self, request, format=None):
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
        
        
        
        