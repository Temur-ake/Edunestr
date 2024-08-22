from django import forms
import re

from apps.models import Contact


class ContactForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '+998 99-999-99-99'})
    )

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'phone', 'email', 'course_type']

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     digits = re.sub(r'\D', '', phone)  # Remove non-digit characters
    #     if len(digits) != 12:
    #         raise forms.ValidationError("Phone number must be 12 digits long.")
    #
    #     # Format phone number
    #     formatted = f"+998 {digits[:2]}-{digits[2:5]}-{digits[5:7]}-{digits[7:]}"
    #     return formatted

# try:
#     contact = Contact.objects.create(
#         name=form.cleaned_data['name'],
#         surname=form.cleaned_data['surname'],
#         phone=form.cleaned_data['phone'],
#         email=form.cleaned_data['email'],
#         course_type=form.cleaned_data['course_type']
#     )
# except Exception as e:
#     print(f"Error saving contact: {e}")
