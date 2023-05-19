from django.urls import path
from .views import (PatientReg, DoctorReg, 
                    Login, LogoutView, AllDoctors,
                    AddMedData, MedStatus, CreateAppointment, AppointmentList, AdminReg
                    , AdminData, AllUsers, GetMyAppointment, Assigned,
                    CreateDocument, CreateDiagForm, MyDiag)

from . import views

urlpatterns = [
    path("patient/reg/", PatientReg.as_view(), name="patient-reg"),
    path("all/users", AllUsers.as_view(), name="all-users"),
    path("doctor/reg/", DoctorReg.as_view(), name="doctor-reg"),
    path("login", Login.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("all/docs", AllDoctors.as_view(), name="all-docs"),
    path("add/med_data", AddMedData.as_view(), name="add-doctor"),
    path("get/status", MedStatus.as_view(), name="get_status"),
    path("create/appointment/<int:medic_id>", CreateAppointment.as_view(), name="appointment"),
    path("get/appointments/", AppointmentList.as_view(), name="appointment-list"),
    path("reg/admin/", AdminReg.as_view(), name="admin"),
    path("admin/data/", AdminData.as_view(), name="admin-data"),
    path("my/appointments/", GetMyAppointment.as_view(), name="get_my_appointments"),
    path("assigned/patients", Assigned.as_view(), name="assigned" ),
    path("add/docs", CreateDocument.as_view(), name="create-doc"),
    path("create/diag/<int:patient_id>", CreateDiagForm.as_view(), name="create-diag"),
    path("my/diag", MyDiag.as_view(), name="my-diagnosis")
]