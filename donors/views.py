
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import (
    DonorProfile,
    BloodRequest,
    PatientBloodRequest,
    BLOOD_GROUPS,
)
from .forms import SignupForm, DonorForm, RequestForm


# Home page
def home(request):
    return render(request, 'home.html', {
        'donor_count': DonorProfile.objects.filter(
            is_available=True
        ).count()
    })


# User registration
def signup(request):
    form = SignupForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')

    return render(request, 'form.html', {
        'form': form,
        'heading': 'Create an account',
        'button': 'Register'
    })


# Donor profile
@login_required
def donor_profile(request):
    profile = DonorProfile.objects.filter(
        user=request.user
    ).first()

    form = DonorForm(
        request.POST or None,
        instance=profile
    )

    if request.method == 'POST' and form.is_valid():
        donor = form.save(commit=False)
        donor.user = request.user
        donor.save()

        messages.success(
            request,
            'Donor profile saved successfully!'
        )
        return redirect('dashboard')

    return render(request, 'form.html', {
        'form': form,
        'heading': 'My donor profile',
        'button': 'Save profile'
    })


# Search available donors
def search(request):
    group = request.GET.get('blood_group', '')
    city = request.GET.get('city', '').strip()[:100]

    donors = DonorProfile.objects.filter(is_available=True)

    if group in dict(BLOOD_GROUPS):
        donors = donors.filter(blood_group=group)

    if city:
        donors = donors.filter(city__icontains=city)

    return render(request, 'search.html', {
        'donors': donors.order_by('-created_at')[:100],
        'groups': BLOOD_GROUPS,
        'group': group,
        'city': city
    })


# Send blood request to a donor
@login_required
def request_blood(request, pk):
    donor = get_object_or_404(
        DonorProfile,
        pk=pk,
        is_available=True
    )

    if donor.user_id == request.user.id:
        messages.error(
            request,
            'You cannot request blood from yourself.'
        )
        return redirect('search')

    form = RequestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        pending = BloodRequest.objects.filter(
            donor=donor,
            requester=request.user,
            status='Pending'
        ).exists()

        if pending:
            messages.error(
                request,
                'You already have a pending request to this donor.'
            )
        else:
            obj = form.save(commit=False)
            obj.requester = request.user
            obj.donor = donor
            obj.save()

            messages.success(
                request,
                'Blood request sent successfully!'
            )
            return redirect('dashboard')

    return render(request, 'form.html', {
        'form': form,
        'heading': f'Request blood from {donor.full_name or donor.user.username}',
        'button': 'Send request'
    })


# Personal user dashboard
@login_required
def dashboard(request):

    sent = BloodRequest.objects.filter(
        requester=request.user
    ).select_related(
        'donor',
        'donor__user'
    ).order_by('-created_at')

    received = BloodRequest.objects.filter(
        donor__user=request.user
    ).select_related(
        'requester',
        'donor'
    ).order_by('-created_at')

    patient_requests = PatientBloodRequest.objects.filter(
        requested_by=request.user
    ).order_by('-created_at')

    profile = DonorProfile.objects.filter(
        user=request.user
    ).first()

    return render(request, 'dashboard.html', {
        'sent': sent,
        'received': received,
        'patient_requests': patient_requests,
        'profile': profile
    })


# Change blood request status
@login_required
@require_POST
def change_status(request, pk):

    item = get_object_or_404(
        BloodRequest,
        pk=pk,
        donor__user=request.user
    )

    new_status = request.POST.get('status')

    valid_transition = (
        item.status == 'Pending'
        and new_status in ('Accepted', 'Rejected')
    ) or (
        item.status == 'Accepted'
        and new_status == 'Completed'
    )

    if valid_transition:
        item.status = new_status
        item.save(update_fields=['status'])

        messages.success(
            request,
            'Request status updated successfully!'
        )
    else:
        messages.error(
            request,
            'Invalid status change.'
        )

    return redirect('dashboard')
