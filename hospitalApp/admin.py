from django.contrib import admin
from .models import Patient, WorkField, Appointment,Service

class WorkFieldAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'area_of_specialist', 'email', 'phone')
    list_filter = ('area_of_specialist', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'phone')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'gender', 'email','image', 'phone', 'body_weight', 'blood_pressure', 'pressure','receptionist','registration_time', 'treated_by', 'treated')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    
    
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'is_confirmed')
    list_filter = ('is_confirmed',)
    search_fields = ('patient__username', 'doctor__username', 'appointment_date')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','description')
    list_filter = ('name', 'price')
    search_fields = ('name', 'description')

admin.site.register(WorkField, WorkFieldAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Service, ServiceAdmin)
