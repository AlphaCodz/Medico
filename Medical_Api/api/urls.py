from django.urls import path
from .views import (PatientReg, DoctorReg, 
                    Login, LogoutView, AllDoctors,
                    AddMedData)

urlpatterns = [
    path("patient/reg/", PatientReg.as_view(), name="patient-reg"),
    path("doctor/reg/", DoctorReg.as_view(), name="doctor-reg"),
    path("login", Login.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("all/docs", AllDoctors.as_view(), name="all-docs"),
    path("add/med_data", AddMedData.as_view(), name="add-doctor")
    # path("appointment/create/<int:medic_id>", CreateAppointment.as_view(), name="appointment")
]
