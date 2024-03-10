from django.db import models

# Create your models here.

from django.db import models
from Patients.models import Patient

# Create your models here.

class Reviews(models.Model):
    user=models.ForeignKey(Patient,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return self.user
    
