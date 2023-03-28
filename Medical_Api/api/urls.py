from django.urls import path
from .views import PatientReg, DoctorReg, Login

urlpatterns = [
    path("patient/reg/", PatientReg.as_view(), name="patient-reg"),
    path("doctor/reg/", DoctorReg.as_view(), name="doctor-reg"),
    path("login", Login.as_view(), name="login")
]
