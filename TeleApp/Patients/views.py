from django.shortcuts import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Patient
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from Doctors.models import Doctor
import razorpay
import hmac
import hashlib


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
    def get(self,request,pk,*args, **kwargs):
        patient=Patient.objects.get(id=pk)
        if patient:
            serializer=PatientProfileSerializer(patient)
            response_data={"patient":serializer.data}
            return Response(response_data,status=status.HTTP_200_OK)
        query_param=request.query_params.get('keywords')
        if query_param:
            doctors=Doctor.objects.filter(department__name__istartswith=query_param).order_by("-average_rating").values('name')
            return Response(doctors,status=status.HTTP_200_OK)
        
    def put(self,request,pk,*args, **kwargs):
        serializer=PatientUpdateSerializer(data=request.data)
        if serializer.is_valid():
            patient=Patient.objects.get(id=pk)
            patient.email=serializer.validated_data['email']
            patient.name=serializer.validated_data['name']
            patient.age=serializer.validated_data['age']
            patient.save()
            return Response({"status":"success"},status=status.HTTP_200_OK)

 
import os

RAZOR_KEY_ID=os.environ.get('razor_id')
RAZOR_KEY_SECRET=os.environ.get('razor_key')
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
client.set_app_details({"title" : "Django", "version" : "5.0.3"})

class PaymentApiView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,pk,*args, **kwargs):
        serializer=PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount=serializer.validated_data['amount']
            currency=serializer.validated_data['currency']
            reciept=serializer.validated_data['receipt']
            try:
                data = { "amount": amount, "currency": currency, "receipt": reciept}
                payment = client.order.create(data=data)
                #id for newly created payment
                razorpay_order_id=payment['id']
                callback_url=f"http://127.0.0.1:8000/patients/{pk}/manage-appointments/payment/handler"
                data['razorpay_order_id']=razorpay_order_id
                data['callback_url']=callback_url
                data['merchant_id']=RAZOR_KEY_ID
                return Response(data,status=status.HTTP_201_CREATED)
            except Exception as e:
                # Handle any exceptions
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#after the successful payment razor pay will send a post request to call back url           
class PaymentHandler(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,pk,*args, **kwargs):
        payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        signature = request.data.get('razorpay_signature')
        result=client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
        })
        if result:
            print("success")
            return Response({"status":"success"})
            
        else:
            print("failed")
            return Response({"status":"failed"},status=status.HTTP_400_BAD_REQUEST)
        
                    




            


 



       

