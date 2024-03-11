from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
  
   class Meta:
        model = Patient
        fields="__all__"
    
class PatientLoginSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(max_length=100)
    class Meta:
        model=Patient
        fields=['email','password','confirm_password']
    
    #object level custom validatioon
    def validate(self,data):
        password=data.get('password')
        confirm_password=data.get('confirm_password')

        if password==confirm_password:
            return data
        else:
            raise serializers.ValidationError("Passwords do not match.")
        
    