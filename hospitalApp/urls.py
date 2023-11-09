from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('user/list/', views.user_list, name='user-list'),
    path('user/create/', views.user_create, name='user-create'),
    path('user/update/<int:user_id>/', views.user_update, name='user-update'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user-delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist-dashboard'),
    path('all/patients/', views.patient_list, name='patient-list'),
    path('appointment-list/', views.appointment_list, name='appointment-list'),
    path('appointments/create/', views.appointment_create, name='appointment-create'),
    
    path('create/service/', views.service_create, name='service-create'),
    path('service/list/', views.service_list, name='service-list'),
    path('service/detail/<int:service_id>/', views.service_detail, name='service-detail'),
    path('<int:service_id>/update/', views.service_update, name='service-update'),
    path('<int:service_id>/delete/', views.service_delete, name='service-delete'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)