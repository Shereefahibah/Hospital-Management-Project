from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    doctordetails = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phonenumber = models.IntegerField(null=True)
    specification = models.CharField(max_length=100, null=True)
    doctorimage=models.ImageField(upload_to="images/")
    def __str__(self):
        return self.doctordetails.first_name

class Patient(models.Model):
    patientdetails = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phonenumber = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, null=True)
    patientimage=models.ImageField(upload_to="images/")
    def __str__(self):
        return self.patientdetails.first_name
        

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, related_name='appointments')
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status_choices = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')