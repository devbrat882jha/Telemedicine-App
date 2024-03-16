from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reviews
from .serializers import HomeSerializer
from django.shortcuts import reverse

class Home(APIView):

    def get(self, request):
        reviews=Reviews.objects.all()[:5]
        patinetregistration_url=reverse("patient-registration")
        patinetlogin_url=reverse("patient-login")
        response_data={"urls":{"patinetregistration_url":patinetregistration_url,
                            "patinetlogin_url":patinetlogin_url}}
        if reviews:
            serializer=HomeSerializer(reviews)
            response_data["reviews"]=serializer.data()
        return Response(response_data,status=status.HTTP_200_OK)


    


       
       
        



