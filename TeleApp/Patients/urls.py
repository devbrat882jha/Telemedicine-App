from django.urls import path
from . import views

urlpatterns = [
    
    path('registration',views.PatientRegistration.as_view(),name='patient-registration'),
    path('login',views.PatientLogin.as_view(),name='patient-login'),
    path('<int:pk>',views.PatientProfile.as_view()),
    path('<int:pk>/manage-appointments/payment',views.PaymentApiView.as_view(),name='manage-appointments')
    ,
    path('<int:pk>/manage-appointments/payment/handler',views.PaymentHandler.as_view(),name='manage-appointments-handler')
      
    
]