from django import forms
from .models import StudentRegistration

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentRegistration
        fields = [
            'full_name', 
            'email', 
            'phone_number', 
            'profile_picture', 
            'date_of_birth', 
            'education', 
            'course', 
            'batch', 
            'experience_level', 
            'comments'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Enter your full name',
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Enter your email address',
                'autocomplete': 'email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Enter your 10-15 digit phone number',
                'autocomplete': 'tel'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input', 
                'type': 'date'
            }),
            'education': forms.Select(attrs={
                'class': 'form-select'
            }),
            'course': forms.Select(attrs={
                'class': 'form-select'
            }),
            'batch': forms.Select(attrs={
                'class': 'form-select'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'placeholder': 'What are your primary goals for joining this class? (Optional)',
                'rows': 4
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing = StudentRegistration.objects.filter(email=email).first()
        if existing and existing.payment_status == 'verified':
            raise forms.ValidationError("A verified registration with this email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Simple validation: remove spaces/dashes and check length
        clean_num = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        if len(clean_num) < 10 or len(clean_num) > 15:
            raise forms.ValidationError("Please enter a valid phone number (10 to 15 digits).")
        return phone_number


class PaymentUploadForm(forms.ModelForm):
    class Meta:
        model = StudentRegistration
        fields = ['payment_screenshot']
        widgets = {
            'payment_screenshot': forms.ClearableFileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*',
            })
        }

    def clean_payment_screenshot(self):
        screenshot = self.cleaned_data.get('payment_screenshot')
        if not screenshot:
            raise forms.ValidationError("Please upload a payment screenshot.")
        return screenshot

