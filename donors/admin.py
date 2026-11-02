
from django.contrib import admin
from .models import DonorProfile, BloodRequest, PatientBloodRequest


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'age',
        'gender',
        'blood_group',
        'contact_number',
        'city',
        'is_available',
    )

    list_filter = (
        'blood_group',
        'city',
        'gender',
        'is_available',
    )

    search_fields = (
        'full_name',
        'contact_number',
        'city',
    )


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'requester',
        'donor',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'requester__username',
        'donor__full_name',
    )


@admin.register(PatientBloodRequest)
class PatientBloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'age',
        'blood_group',
        'units_required',
        'hospital_name',
        'city',
        'urgency',
        'status',
    )

    list_filter = (
        'blood_group',
        'urgency',
        'status',
        'city',
    )

    search_fields = (
        'patient_name',
        'hospital_name',
        'contact_number',
    )
