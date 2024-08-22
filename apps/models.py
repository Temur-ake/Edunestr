# models.py
from django.db import models
from django.db.models import CharField, ImageField, Model, TextField, ForeignKey, CASCADE, Choices

from django.core.validators import RegexValidator, EmailValidator
from phonenumber_field.modelfields import PhoneNumberField


# models.py


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    list_image = models.ImageField(upload_to='courses/')
    detail_image = models.ImageField(upload_to='courses/images/', blank=True, null=True)  # Optional image field
    detail_video = models.FileField(upload_to='courses/videos/', blank=True, null=True)  # Optional video field

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(
        max_length=254,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    course_type = models.ForeignKey(Course, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Teacher(models.Model):
    COURSE_TYPE_CHOICES = [
        ('IELTS 8', 'IELTS 8'),
        ('IELTS 7.5', 'IELTS 7.5'),
        ('IELTS 7', 'IELTS 7'),
        ('IELTS 6.5', 'IELTS 6.5'),
        ('IELTS 6', 'IELTS 6'),
    ]
    full_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teachers/images/', blank=True, null=True)  # Optional image field
    video = models.FileField(upload_to='teachers/videos/', blank=True, null=True)  # Optional video field
    job_field = models.CharField(max_length=255, choices=COURSE_TYPE_CHOICES)

    def __str__(self):
        return self.full_name

# class CourseImage(Model):
#     image = ImageField(upload_to='products/')
#     course = ForeignKey('apps.Course', CASCADE, related_name='images')


# course_types = Contact.objects.values_list('course_type', flat=True).distinct()
# print(course_types)
