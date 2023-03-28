from django.shortcuts import render
from helpers.views import BaseView
from .models import PrimaryUser, Appointment
from rest_framework.response import Response
from rest_framework.decorators import APIView

# Create your views here.
class PatientReg(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "password"]
    def post(self, request, format=None):
        conn = super().post(request, format)
        if not conn:
            resp = {
                "code": 400,
                "message": "Connection Error"
            }
            return Response(resp, 400)
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
        
            
        
        
        