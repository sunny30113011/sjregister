from django.db import models

class StudentRegistration(models.Model):
    COURSE_CHOICES = [
        ('fullstack', 'Full Stack Web Development'),
        ('python_django', 'Python & Django Backend'),
        ('ds_ml', 'Data Science & Machine Learning'),
        ('ui_ux', 'UI/UX Design'),
        ('cybersecurity', 'Cybersecurity'),
    ]

    BATCH_CHOICES = [
        ('morning', 'Morning Batch (8:00 AM - 10:00 AM)'),
        ('afternoon', 'Afternoon Batch (2:00 PM - 4:00 PM)'),
        ('evening', 'Evening Batch (6:00 PM - 8:00 PM)'),
        ('weekend', 'Weekend Batch (Sat & Sun, 10:00 AM - 1:00 PM)'),
    ]

    EDUCATION_CHOICES = [
        ('high_school', 'High School / Intermediate'),
        ('undergraduate', 'Undergraduate Student'),
        ('graduate', 'Graduate'),
        ('postgraduate', 'Postgraduate'),
        ('other', 'Other'),
    ]

    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (No prior coding experience)'),
        ('intermediate', 'Intermediate (Some coding knowledge)'),
        ('advanced', 'Advanced (Proficient / Professional)'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        verbose_name="Profile Picture (User Pic)",
        help_text="Please upload a passport size photo of yourself"
    )
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    education = models.CharField(
        max_length=20, 
        choices=EDUCATION_CHOICES, 
        verbose_name="Educational Qualification"
    )
    course = models.CharField(
        max_length=20, 
        choices=COURSE_CHOICES, 
        verbose_name="Chosen Course"
    )
    batch = models.CharField(
        max_length=20, 
        choices=BATCH_CHOICES, 
        verbose_name="Preferred Batch"
    )
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_CHOICES, 
        verbose_name="Programming Experience"
    )
    comments = models.TextField(
        blank=True, 
        verbose_name="Additional Comments / Learning Goals",
        help_text="Tell us what you hope to achieve in this course"
    )
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated Date")
    payment_screenshot = models.ImageField(
        upload_to='payment_screenshots/', 
        blank=True, 
        null=True, 
        verbose_name="Payment Screenshot",
        help_text="Upload the screenshot of the QR code payment"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Payment'),
            ('paid', 'Paid (Pending Verification)'),
            ('verified', 'Payment Verified')
        ],
        default='pending',
        verbose_name="Payment Status"
    )

    def send_verification_email(self):
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = "Admission Confirmed - SJ Tech Classes"
        message = (
            f"Dear {self.full_name},\n\n"
            f"We are pleased to inform you that your payment has been successfully verified! "
            f"Your admission to the course '{self.get_course_display()}' is now confirmed.\n\n"
            f"Here is a summary of your registration:\n"
            f"----------------------------------------\n"
            f"Registration ID : #SJ-{self.id:04d}\n"
            f"Course          : {self.get_course_display()}\n"
            f"Preferred Batch : {self.get_batch_display()}\n"
            f"----------------------------------------\n\n"
            f"Our admissions officer will contact you shortly to coordinate the orientation session "
            f"and share your student portal credentials.\n\n"
            f"If you have any questions or require support, please reply to this email or write to us "
            f"at support@sjtechclasses.com.\n\n"
            f"Welcome to SJ Tech!\n\n"
            f"Best regards,\n"
            f"Admissions Office\n"
            f"SJ Tech Classes"
        )
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send verification email to {self.email}: {e}")

    def save(self, *args, **kwargs):
        is_verified_now = False
        if self.pk:
            old_instance = StudentRegistration.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.payment_status != 'verified' and self.payment_status == 'verified':
                is_verified_now = True
        elif self.payment_status == 'verified':
            is_verified_now = True
            
        super().save(*args, **kwargs)
        
        if is_verified_now:
            self.send_verification_email()

    def __str__(self):
        return f"{self.full_name} - {self.get_course_display()}"

    class Meta:
        verbose_name = "Student Registration"
        verbose_name_plural = "Student Registrations"
        ordering = ['-registered_at']



