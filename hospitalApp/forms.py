from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Appointment, Service, DoctorNote

class BootstrapStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control col-md-12'})
            
class SignUpForm(UserCreationForm, BootstrapStyleForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':'use your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter password'}))
    class Meta:
        fields = ['username', 'password']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'reason', 'is_confirmed']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control col-md-6'}),  # Apply Bootstrap styling to the patient field
            'doctor': forms.Select(attrs={'class': 'form-control col-md-6'}),  # Apply Bootstrap styling to the doctor field
            'appointment_date': forms.DateInput(attrs={'class': 'form-control col-md-6', 'type': 'date'}),  # Apply Bootstrap styling to the date field
            'reason': forms.Textarea(attrs={'class': 'form-control col-md-6', 'rows': 3}),  # Apply Bootstrap styling to the reason field
            'is_confirmed': forms.CheckboxInput(attrs={'class': 'form-check-input col-md-1'}),  # Apply Bootstrap styling to the checkbox widget
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
    }

    labels = {
        'name': 'Service Name',
        'description': 'Description',
        'price': 'Price',
    }



class DoctorNoteForm(forms.ModelForm):
    class Meta:
        model = DoctorNote
        fields = ['patient', 'doctor', 'symptoms']
        widgets = {
            'patient': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
        }
