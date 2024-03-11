from django.urls import path
from . import views

urlpatterns = [
    
    path('registration',views.PatientRegistration.as_view(),name='PatientRegistration')
]