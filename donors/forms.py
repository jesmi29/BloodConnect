
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import DonorProfile, BloodRequest, PatientBloodRequest


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        }),
        min_length=8
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email address'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class DonorForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        exclude = ['user', 'created_at']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name'
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'Enter your age',
                'min': 1,
                'max': 100
            }),
            'gender': forms.Select(choices=[
                ('', 'Select Gender'),
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other'),
            ]),
            'blood_group': forms.Select(),
            'contact_number': forms.TextInput(attrs={
                'placeholder': 'Enter contact number'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Enter your city'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter your address',
                'rows': 3
            }),
            'is_available': forms.CheckboxInput(),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age is not None and (age < 1 or age > 100):
            raise forms.ValidationError(
                'Please enter a valid age.'
            )

        return age

    def clean_contact_number(self):
        number = self.cleaned_data.get('contact_number', '').strip()

        if number:
            digits = ''.join(char for char in number if char.isdigit())

            if len(digits) < 10 or len(digits) > 15:
                raise forms.ValidationError(
                    'Enter a valid contact number with 10 to 15 digits.'
                )

            if any(char not in '+0123456789 -()' for char in number):
                raise forms.ValidationError(
                    'Contact number contains invalid characters.'
                )

        return number

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()

        if not city:
            raise forms.ValidationError(
                'Please enter your city.'
            )

        return city


class RequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        exclude = [
            'requester',
            'donor',
            'status',
            'created_at'
        ]

        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'Enter your blood request message',
                'rows': 4
            }),
        }


class PatientBloodRequestForm(forms.ModelForm):
    class Meta:
        model = PatientBloodRequest
        exclude = [
            'requested_by',
            'status',
            'created_at'
        ]

        widgets = {
            'patient_name': forms.TextInput(attrs={
                'placeholder': 'Enter patient name'
            }),
            'age': forms.NumberInput(attrs={
                'min': 1,
                'max': 120
            }),
            'contact_number': forms.TextInput(attrs={
                'placeholder': 'Enter contact number'
            }),
            'blood_group': forms.Select(),
            'units_required': forms.NumberInput(attrs={
                'min': 1
            }),
            'hospital_name': forms.TextInput(attrs={
                'placeholder': 'Enter hospital name'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Enter city'
            }),
            'required_date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate().isoformat()

        self.fields['required_date'].widget.attrs['min'] = today

    def clean_required_date(self):
        required_date = self.cleaned_data.get('required_date')

        if required_date and required_date < timezone.localdate():
            raise forms.ValidationError(
                'Required date cannot be in the past. Please select today or a future date.'
            )

        return required_date
