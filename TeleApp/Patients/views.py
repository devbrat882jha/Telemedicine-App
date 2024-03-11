from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PatientSerializer
from rest_framework import status

# Create your views here.
class PatientRegistration(APIView):
    def post(self, request, *args, **kwargs):
        # Access the request data
        request_data = request.data
        serializer=PatientSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

       

