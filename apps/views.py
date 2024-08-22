from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin
# views.py
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
# from twilio.rest import Client

from root.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
from .forms import ContactForm
from .models import Contact
# from .forms import ContactForm
from .models import Course, Teacher
import logging

logger = logging.getLogger(__name__)


# views.py


def combined_list_view(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    context = {
        'courses': courses,
        'teachers': teachers,
    }
    return render(request, 'homepage_3.html', context)


def contact_success(request):
    return render(request, 'contact.html')


class ContactCreateView(CreateView):
    template_name = 'homepage_3.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        contact = form.save()
        try:
            send_mail(
                'New Contact Form Submission',
                f"Name: {contact.name}\nSurname: {contact.surname}\nPhone: {contact.phone}\nEmail: {contact.email}\nCourse Type: {contact.course_type}\nCreated At: {contact.created_at}",
                f'{contact.email}',
                ['kozimovt0@gmail.com'],
                fail_silently=False,
            )
        except BadHeaderError:
            logger.error("Invalid header found.")
        except SMTPException as e:
            logger.error(f"SMTP error occurred: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        return super().form_valid(form)


class AdminView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'admin_view.html'
    context_object_name = 'contacts'
    login_url = '/login/'  # Optional: Redirect to login page if not authenticated


import pytz
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from .models import Contact


def download_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define data for the table
    contacts = Contact.objects.all()
    data = [['Name', 'Surname', 'Phone', 'Email', 'Course Type', 'Created At']]

    # Define the timezone
    tz = pytz.timezone('Asia/Tashkent')

    for contact in contacts:
        # Convert contact created_at to Asia/Tashkent timezone
        created_at = contact.created_at.astimezone(tz)
        data.append([
            contact.name,
            contact.surname,
            contact.phone,
            contact.email,
            contact.course_type,
            created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    # Create a table
    table = Table(data)

    # Add some styling
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#333'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), '#f4f4f4'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ])
    table.setStyle(style)

    # Build the PDF
    elements = [table]
    doc.build(elements)

    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contacts.pdf"'
    return response
