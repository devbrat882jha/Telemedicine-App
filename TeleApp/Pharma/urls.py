from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.Pharma.as_view(),name='Pharma')
]