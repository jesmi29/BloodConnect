
from django.db import models
from django.contrib.auth.models import User


BLOOD_GROUPS = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]


class DonorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=20, null=True)

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUPS
    )

    contact_number = models.CharField(
        max_length=20,
        null=True,
        help_text='Private: not displayed in search results'
    )

    city = models.CharField(max_length=100)
    address = models.TextField(null=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )

    donor = models.ForeignKey(
        DonorProfile,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )

    message = models.TextField(max_length=500)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} - {self.donor.full_name}"


class PatientBloodRequest(models.Model):
    URGENCY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Emergency', 'Emergency'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    contact_number = models.CharField(max_length=15)

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUPS
    )

    units_required = models.PositiveIntegerField()
    hospital_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)

    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        default='Normal'
    )

    required_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"
