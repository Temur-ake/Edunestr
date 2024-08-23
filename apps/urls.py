from django.urls import path
from django.contrib.auth import views as auth_views

from apps.views import contact_success, ContactCreateView, combined_list_view, AdminView, download_pdf

urlpatterns = [
    path('', combined_list_view, name='h3'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('contact-success/', contact_success, name='contact-success'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('staff/admin/', AdminView.as_view(), name='admin_view'),
    path('download-pdf/', download_pdf, name='download_pdf'),
]


