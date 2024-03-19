from rest_framework import serializers
from .models import Patient
import re


def password_validator(password):
    pattern = "^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]+$"
    match = re.match(pattern, password)
    if not match:
        raise  serializers.ValidationError(
            'Password must contain at least one number and one of the following special characters: !@#$%^&*')
    


class PatientSerializer(serializers.ModelSerializer):
   confirm_password = serializers.CharField(write_only=True)
   password=serializers.CharField(validators=[password_validator])
   class Meta:
        model = Patient
        fields=['id','email','password','name','age','doctor','confirm_password']
    
   
   #object level validation
   def validate(self,data):
        password=data.get('password')
        confirm_password=data.get('confirm_password')
        if password!=confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        #confirm field is not required in database
        data.pop('confirm_password')
        return data
    
#we did not used model serialiser as it would have put validators of model fields 
   
class PatientLoginSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=50)

class PatientProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model=Patient
       exclude = ['password']


class PaymentSerializer(serializers.Serializer):
    amount=serializers.FloatField()
    currency=serializers.CharField(max_length=10,default='INR')
    receipt = serializers.CharField(max_length=255)

    def update(self, data):
       amount=data.get('amount')*1000
       return data
    


    

    
   
        
    