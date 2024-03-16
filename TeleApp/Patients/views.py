from django.shortcuts import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Patient
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PatientSerializer, PatientLoginSerializer,PatientProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


def get_tokens_for_user(patient):
    refresh = RefreshToken.for_user(patient)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class PatientRegistration(APIView):
    def get(self, request):
        url = reverse('patient-login')
        return Response({"url": url})

    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            token = get_tokens_for_user(patient)
            return Response(
                {"token": token, 'message': 'Registered successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientLogin(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                patient = Patient.objects.get(email=email)
            except Patient.DoesNotExist:
                return Response(
                    {"msg": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if check_password(password, patient.password):
                token = get_tokens_for_user(patient)
                return Response(
                    {"token": token, "msg": "You are logged in"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"msg": "Wrong password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#TokenAuthentication class is for django inbuilt authentication
class PatientProfile(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        patient=Patient.objects.get(id=pk)
        if patient:
            serializer=PatientProfileSerializer(data=patient)
            response_data={"patient":serializer.data}
            return Response(response_data,status=status.HTTP_200_OK)
        query_param=request.query_params.get('keywords')
        if query_param:
            pass


 



       

