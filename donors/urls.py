
from django.urls import path
from . import views
from . import hospital_views

urlpatterns = [
    # Normal user pages
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.donor_profile, name='donor_profile'),
    path('search/', views.search, name='search'),
    path('request/<int:pk>/', views.request_blood, name='request_blood'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('status/<int:pk>/', views.change_status, name='change_status'),

    # Patient and donor pages
    path(
        'patient/request/',
        hospital_views.patient_request,
        name='patient_request'
    ),
    path(
        'donor/search/',
        hospital_views.donor_search,
        name='donor_search'
    ),

    # Hospital pages
    path(
        'hospital/dashboard/',
        hospital_views.hospital_dashboard,
        name='hospital_dashboard'
    ),
    path(
        'hospital/export/',
        hospital_views.export_excel,
        name='export_excel'
    ),
    path(
        'hospital/patient-status/<int:pk>/',
        hospital_views.update_patient_status,
        name='update_patient_status'
    ),
    path(
        'hospital/donor-contact/<int:pk>/',
        hospital_views.view_donor_contact,
        name='view_donor_contact'
    ),

    # Hospital donor management
    path(
        'hospital/donors/',
        hospital_views.manage_donors,
        name='manage_donors'
    ),
    path(
        'hospital/donor-availability/<int:pk>/',
        hospital_views.update_donor_availability,
        name='update_donor_availability'
    ),
    path(
        'hospital/donor-delete/<int:pk>/',
        hospital_views.delete_donor,
        name='delete_donor'
    ),
]
