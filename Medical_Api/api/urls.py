from django.urls import path
from .views import (PatientReg, DoctorReg, 
                    Login, LogoutView, AllDoctors,
                    AddMedData, MedStatus, CreateAppointment)

urlpatterns = [
    path("patient/reg/", PatientReg.as_view(), name="patient-reg"),
    path("doctor/reg/", DoctorReg.as_view(), name="doctor-reg"),
    path("login", Login.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("all/docs", AllDoctors.as_view(), name="all-docs"),
    path("add/med_data", AddMedData.as_view(), name="add-doctor"),
    path("get/status", MedStatus.as_view(), name="get_status"),
    path("create/appointment/<int:medic_id>", CreateAppointment.as_view(), name="appointment")
]
