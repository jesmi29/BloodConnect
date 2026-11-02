
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST

from openpyxl import Workbook

from .models import DonorProfile, BloodRequest, PatientBloodRequest
from .forms import PatientBloodRequestForm


# Patient blood request form
def patient_request(request):
    form = PatientBloodRequestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        patient = form.save(commit=False)

        if request.user.is_authenticated:
            patient.requested_by = request.user

        patient.save()

        messages.success(
            request,
            'Patient blood request submitted successfully!'
        )
        return redirect('dashboard')

    return render(request, 'form.html', {
        'form': form,
        'heading': 'Patient Blood Request',
        'button': 'Submit Request'
    })


# Search donors
def donor_search(request):
    blood_group = request.GET.get('blood_group', '')
    city = request.GET.get('city', '').strip()

    donors = DonorProfile.objects.filter(is_available=True)

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    if city:
        donors = donors.filter(city__icontains=city)

    return render(request, 'search.html', {
        'donors': donors.order_by('-created_at'),
        'groups': DonorProfile._meta.get_field(
            'blood_group'
        ).choices,
        'group': blood_group,
        'city': city
    })


# Hospital dashboard
@staff_member_required
def hospital_dashboard(request):

    patient_requests = PatientBloodRequest.objects.all().order_by(
        '-created_at'
    )

    blood_group = request.GET.get('blood_group', '')
    city = request.GET.get('city', '').strip()
    urgency = request.GET.get('urgency', '')
    search = request.GET.get('search', '').strip()

    if blood_group:
        patient_requests = patient_requests.filter(
            blood_group=blood_group
        )

    if city:
        patient_requests = patient_requests.filter(
            city__icontains=city
        )

    if urgency:
        patient_requests = patient_requests.filter(
            urgency=urgency
        )

    if search:
        patient_requests = patient_requests.filter(
            Q(patient_name__icontains=search) |
            Q(hospital_name__icontains=search)
        )

    available_donors = DonorProfile.objects.filter(
        is_available=True
    ).order_by('-created_at')

    context = {
        'total_donors': DonorProfile.objects.count(),
        'total_patients': PatientBloodRequest.objects.values(
            'patient_name'
        ).distinct().count(),
        'total_requests': PatientBloodRequest.objects.count(),
        'pending_requests': PatientBloodRequest.objects.filter(
            status='Pending'
        ).count(),

        'patient_requests': patient_requests,
        'available_donors': available_donors,

        'blood_groups': DonorProfile._meta.get_field(
            'blood_group'
        ).choices,

        'urgency_choices': PatientBloodRequest.URGENCY_CHOICES,

        'selected_blood_group': blood_group,
        'selected_city': city,
        'selected_urgency': urgency,
        'search': search,
    }

    return render(
        request,
        'donors/hospital_dashboard.html',
        context
    )


# View donor contact - hospital staff only
@staff_member_required
def view_donor_contact(request, pk):

    donor = get_object_or_404(
        DonorProfile,
        pk=pk,
        is_available=True
    )

    return JsonResponse({
        'contact_number': donor.contact_number or 'Not provided'
    })


# Export Excel report
@staff_member_required
def export_excel(request):

    workbook = Workbook()

    # Donors sheet
    donor_sheet = workbook.active
    donor_sheet.title = 'Donors'

    donor_sheet.append([
        'Donor Name',
        'Username',
        'Age',
        'Gender',
        'Blood Group',
        'Contact Number',
        'City',
        'Availability'
    ])

    for donor in DonorProfile.objects.select_related('user').all():
        donor_sheet.append([
            donor.full_name,
            donor.user.username,
            donor.age,
            donor.gender,
            donor.blood_group,
            donor.contact_number,
            donor.city,
            'Available' if donor.is_available else 'Unavailable'
        ])

    # Patient requests sheet
    patient_sheet = workbook.create_sheet('Patient Requests')

    patient_sheet.append([
        'Patient Name',
        'Age',
        'Contact Number',
        'Blood Group',
        'Units Required',
        'Hospital Name',
        'City',
        'Urgency',
        'Required Date',
        'Status'
    ])

    for patient in PatientBloodRequest.objects.all():
        patient_sheet.append([
            patient.patient_name,
            patient.age,
            patient.contact_number,
            patient.blood_group,
            patient.units_required,
            patient.hospital_name,
            patient.city,
            patient.urgency,
            patient.required_date,
            patient.status
        ])

    # Blood requests sheet
    request_sheet = workbook.create_sheet('Blood Requests')

    request_sheet.append([
        'Requester',
        'Donor',
        'Blood Group',
        'Donor City',
        'Message',
        'Status',
        'Created At'
    ])

    for blood_request in BloodRequest.objects.select_related(
        'requester',
        'donor'
    ).all():
        request_sheet.append([
            blood_request.requester.username,
            blood_request.donor.full_name,
            blood_request.donor.blood_group,
            blood_request.donor.city,
            blood_request.message,
            blood_request.status,
            blood_request.created_at.strftime('%d-%m-%Y %H:%M')
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename="BloodConnect_Report.xlsx"'
    )

    workbook.save(response)

    return response


# Update patient request status
@staff_member_required
@require_POST
def update_patient_status(request, pk):

    item = get_object_or_404(
        PatientBloodRequest,
        pk=pk
    )

    new_status = request.POST.get('status')

    valid_transition = (
        item.status == 'Pending'
        and new_status in ('Accepted', 'Cancelled')
    ) or (
        item.status == 'Accepted'
        and new_status in ('Completed', 'Cancelled')
    )

    if valid_transition:
        item.status = new_status
        item.save(update_fields=['status'])

        messages.success(
            request,
            'Patient request status updated successfully!'
        )
    else:
        messages.error(
            request,
            'Invalid status change.'
        )

    return redirect('hospital_dashboard')


# Hospital donor management
@staff_member_required
def manage_donors(request):

    donors = DonorProfile.objects.select_related(
        'user'
    ).all().order_by('-created_at')

    search = request.GET.get('search', '').strip()
    availability = request.GET.get('availability', '')

    if search:
        donors = donors.filter(
            Q(full_name__icontains=search) |
            Q(user__username__icontains=search) |
            Q(city__icontains=search)
        )

    if availability == 'available':
        donors = donors.filter(is_available=True)

    elif availability == 'unavailable':
        donors = donors.filter(is_available=False)

    return render(request, 'donors/manage_donors.html', {
        'donors': donors,
        'search': search,
        'availability': availability,
    })


# Update donor availability
@staff_member_required
@require_POST
def update_donor_availability(request, pk):

    donor = get_object_or_404(
        DonorProfile,
        pk=pk
    )

    donor.is_available = not donor.is_available

    donor.save(update_fields=['is_available'])

    messages.success(
        request,
        'Donor availability updated successfully!'
    )

    return redirect('manage_donors')


# Delete donor
@staff_member_required
@require_POST
def delete_donor(request, pk):

    donor = get_object_or_404(
        DonorProfile,
        pk=pk
    )

    donor.delete()

    messages.success(
        request,
        'Donor deleted successfully!'
    )

    return redirect('manage_donors')
