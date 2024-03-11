from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PatientSerializer,PatientLoginSerializer
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import check_password
from .models import Patient

# Create your views here.
class PatientRegistration(APIView):
    def get(self,request):
        url=reverse('patients-login')
        return Response({"url":url})
    
    def post(self, request, *args, **kwargs):
        # Access the request data
        request_data = request.data
        serializer=PatientSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class PatientLogin(APIView):
    def post(self,request,*args,**kwargs):
        request_data=request.data
        serializer=PatientLoginSerializer(data=request_data)
        if serializer.is_valid:
            email=serializer.data['email']
            password=serializer.data['password']
            hashed_password_in_db=Patient.objects.get(email=email).password
            if check_password(password, hashed_password_in_db):
                print("login succesful")





       

