from django.db import models
from Patients.models import Patient

# Create your models here.

class Reviews(models.Model):
    user=models.ForeignKey(Patient,on_delete=models.CASCADE)
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    #ordering model instances as per lated review updated

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return self.user



    
