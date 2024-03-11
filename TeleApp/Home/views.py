from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Reviews
from .serializers import HomeSerializer

class Home(APIView):

    def get(self, request):
        
        reviews=Reviews.objects.all()
        serializer=HomeSerializer(reviews)
        data=serializer.data()
        return Response(data,status=200)
    
    


       
       
        



