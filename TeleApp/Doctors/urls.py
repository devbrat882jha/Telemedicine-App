from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.Doctor.as_view(),name='Doctor'),
    
]