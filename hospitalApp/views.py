from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.conf import settings
from .forms import SignUpForm, EmailAuthenticationForm
from .models import Patient, Appointment,Service, WorkField, DoctorNote
from .forms import AppointmentForm, ServiceForm, DoctorNoteForm
from django.http import JsonResponse
from .models import Patient


def home(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Redirect to your home page
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user-list')

    return render(request, 'user_update.html', {'user': user})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user-list')


@login_required
def doctor_dashboard(request):
    treated_patients = Patient.objects.filter(treated=True)
    # Count treated patients
    treated_patients_count = Patient.objects.filter(treated=True).count()

    # Count appointments
    appointments_count = Appointment.objects.count()

    # Count pending patients
    pending_patients_count = Patient.objects.filter(treated=False).count()

    # Count rejected patients (if you have a field to indicate rejection)
    # rejected_patients_count = Patient.objects.filter(rejected=True).count()

    context = {
        'treated_patients': treated_patients,
        'treated_patients_count': treated_patients_count,
        'appointments_count': appointments_count,
        'pending_patients_count': pending_patients_count,
        # 'rejected_patients_count': rejected_patients_count,
    }

    return render(request, 'doctor_dashboard.html', context)

@login_required
def receptionist_dashboard(request):
    patients = Patient.objects.all()
    return render(request, 'receptionist_dashboard.html', {'patients': patients})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Get the patient and doctor instances based on user input (form data)
            patient_name = form.cleaned_data['patient']  # Assuming the form provides the user ID
            doctor_name = form.cleaned_data['doctor']  # Assuming the form provides the user ID
            
            # Retrieve the user instances based on the names
            patient = User.objects.get(username=patient_name)
            doctor = User.objects.get(username=doctor_name)
            
            appointment_date = form.cleaned_data['appointment_date']
            reason = form.cleaned_data['reason']
            appointment = Appointment(patient=patient, doctor=doctor, appointment_date=appointment_date, reason=reason)
            appointment.save()
            return redirect('appointment-list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_create.html', {'form': form})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})


##################
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service-list')
    else:
        form = ServiceForm()
    return render(request, 'service_create.html', {'form': form})

def service_list(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'service_list.html', context)

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})

def service_update(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service-list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_update.html', {'form': form})

def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('service-list')
    return render(request, 'service_delete.html', {'service': service})


@login_required
def patient_create_note(request, patient_id):
    if request.method == 'POST':
        form = DoctorNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient-detail-note', patient_id=patient_id)
    else:
        form = DoctorNoteForm(initial={'patient': patient_id, 'doctor': request.user.id})
    return render(request, 'patient_create_note.html', {'form': form})


@login_required
def patient_detail_note(request, patient_id):
    patient_notes = DoctorNote.objects.filter(patient_id=patient_id)
    return render(request, 'patient_detail_note.html', {'patient_notes': patient_notes, 'patient_id': patient_id})

@login_required
def patient_update_note(request, note_id):
    note = get_object_or_404(DoctorNote, id=note_id)
    if request.method == 'POST':
        form = DoctorNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('patient-detail-note', patient_id=note.patient_id)
    else:
        form = DoctorNoteForm(instance=note)
    return render(request, 'patient_update_note.html', {'form': form, 'note': note})

@login_required
def patient_delete_note(request, note_id):
    note = get_object_or_404(DoctorNote, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('patient-detail-note', patient_id=note.patient_id)
    return render(request, 'patient_delete_note.html', {'note': note})