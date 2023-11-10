from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
WORK_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Receptionist', 'Receptionist'),
    ]


class CommonFields(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='profile_images/', default='default/default.jpg')
    class Meta:
        abstract = True  # This is an abstract base class to share common fields

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class WorkField(CommonFields):
    area_of_specialist = models.CharField(max_length=50, choices=WORK_CHOICES)

class Patient(CommonFields):
    body_weight = models.DecimalField(max_digits=5, decimal_places=2)  # Example: DecimalField for body weight
    blood_pressure = models.CharField(max_length=15)  # Example: CharField for blood pressure
    pressure = models.CharField(max_length=15)  # Example: CharField for pressure
    receptionist = models.ForeignKey(WorkField, on_delete=models.CASCADE, limit_choices_to={'area_of_specialist': 'Receptionist'})
    registration_time = models.DateTimeField(auto_now_add=True)
    treated_by = models.ForeignKey(WorkField, on_delete=models.CASCADE, limit_choices_to={'area_of_specialist': 'Doctor'}, related_name='patients_treated')
    treated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Registration for {self.first_name} by {self.receptionist.first_name} at {self.registration_time}"

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment with {self.patient.username} on {self.appointment_date}'

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class DoctorNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(WorkField, on_delete=models.CASCADE)
    note_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    
    def is_doctor(self):
        return self.doctor.area_of_specialist == 'Doctor'

    def __str__(self):
        specialist_type = "Doctor" if self.is_doctor() else "Receptionist"
        return f"Note for {self.patient.first_name} by {specialist_type} {self.doctor.first_name} on {self.note_date}"
