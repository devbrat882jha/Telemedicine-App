from django.db import models
from Patients.models import *
from django.contrib.auth.hashers import make_password


# Create your models here.


class Doctor(models.Model):
    name=models.CharField(max_length=50)
    total_experience=models.IntegerField(default=0)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    average_rating = models.FloatField(default=0)
    

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    #updating average rating before saving to database
    def update_average_rating(self):
        ratings=Rating.objects.filter(doctor=self)
        if ratings:
            self.average_rating=sum(rating.rating for rating in ratings)/ratings.count()
        else:
            self.average_rating=0
        self.save()

    def __str__(self):
        return self.name





class DoctorLocation(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='doctor')
    station_name=models.CharField(max_length=250)
    latitude=models.FloatField()
    longitude=models.FloatField()

    def __str__(self):
        return self.station_name
