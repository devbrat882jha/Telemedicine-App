from django.db import models
from Doctors.models import Doctor
from django.contrib.auth.hashers import make_password

# Create your models here.


class Patient(models.Model):
    email=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    doctor=models.ManyToManyField(Doctor,
                                  related_name='doctors')
    

    def save(self, *args, **kwargs):
        # Hash the password before saving
        
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        
class Rating(models.Model):
    rating=models.FloatField(default=0.00)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='patient')
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="rating")


class PatientLocation(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    station_name=models.CharField(max_length=250)
    latitude=models.FloatField()
    longitude=models.FloatField()

    def __str__(self):
        return self.station_name


class PatientHealthRecord(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    height=models.FloatField()
    weight=models.FloatField()

#PatientHealthRecord related tables
    
class BloodPressure(models.Model):
    related_health_record=models.ForeignKey(PatientHealthRecord,on_delete=models.CASCADE)
    mm=models.IntegerField()
    Hg=models.IntegerField()
    time=models.DateTimeField()

    def __str__(self):
        return f"BP :{self.mm}/{self.Hg}"


class DieseaseHistory(models.Model):
    related_health_record=models.ForeignKey(PatientHealthRecord,on_delete=models.CASCADE)
    disease_name=models.CharField(max_length=100)
    doctor=models.CharField(max_length=50)
    duration=models.FloatField()

#table related to medical history
    
class MedicationsHistory(models.Model):
    name=models.CharField(max_length=100)
    dose=models.CharField(max_length=20)
    disease=models.ForeignKey(DieseaseHistory,on_delete=models.CASCADE)
    