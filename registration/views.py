from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentRegistration
from .forms import StudentRegistrationForm, PaymentUploadForm

def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            existing = StudentRegistration.objects.filter(email=email).first()
            if existing:
                # Update existing pending registration
                for field in form.cleaned_data:
                    if field == 'profile_picture' and not request.FILES.get('profile_picture'):
                        continue
                    setattr(existing, field, form.cleaned_data[field])
                existing.payment_status = 'pending'
                existing.save()
                student = existing
            else:
                student = form.save()
            
            return redirect('registration:payment', student_id=student.id)
    else:
        form = StudentRegistrationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)

def payment_view(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)
    
    # If payment is already verified, bypass the page
    if student.payment_status == 'verified':
        return redirect('registration:success', student_id=student.id)
        
    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.payment_status = 'paid'  # Update status to paid, awaiting verification
            student.save()
            return redirect('registration:success', student_id=student.id)
    else:
        form = PaymentUploadForm(instance=student)
        
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'registration/payment.html', context)

def success_view(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)
    context = {
        'student': student,
    }
    return render(request, 'registration/success.html', context)
