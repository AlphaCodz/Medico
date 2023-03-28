from django.urls import path
from .views import PatientReg

urlpatterns = [
    path("patient/reg/", PatientReg.as_view(), name="patient-reg")
]
