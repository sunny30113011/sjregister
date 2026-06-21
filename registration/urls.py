from django.urls import path
from .views import register_view, payment_view, success_view

app_name = 'registration'

urlpatterns = [
    path('', register_view, name='register'),
    path('payment/<int:student_id>/', payment_view, name='payment'),
    path('success/<int:student_id>/', success_view, name='success'),
]

