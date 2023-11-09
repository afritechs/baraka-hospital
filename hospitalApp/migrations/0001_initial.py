# Generated by Django 4.1.7 on 2023-11-08 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='WorkField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image', models.ImageField(default='default/default.jpg', upload_to='profile_images/')),
                ('area_of_specialist', models.CharField(choices=[('Doctor', 'Doctor'), ('Receptionist', 'Receptionist')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image', models.ImageField(default='default/default.jpg', upload_to='profile_images/')),
                ('body_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('blood_pressure', models.CharField(max_length=15)),
                ('pressure', models.CharField(max_length=15)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('treated', models.BooleanField(default=False)),
                ('receptionist', models.ForeignKey(limit_choices_to={'area_of_specialist': 'Receptionist'}, on_delete=django.db.models.deletion.CASCADE, to='hospitalApp.workfield')),
                ('treated_by', models.ForeignKey(limit_choices_to={'area_of_specialist': 'Doctor'}, on_delete=django.db.models.deletion.CASCADE, related_name='patients_treated', to='hospitalApp.workfield')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField(auto_now_add=True)),
                ('reason', models.TextField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]