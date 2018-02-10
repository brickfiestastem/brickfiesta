from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        send_mail("Brick Fiesta Contact Us",
                  self.cleaned_data['message'],
                  self.cleaned_data['email'],
                  ['customer.support@brickfiesta.com'],
                  fail_silently=False)
        pass