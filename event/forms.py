from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        send_mail(subject="Brick Fiesta - Contact Us",
                  message=self.cleaned_data['message'],
                  from_email=self.cleaned_data['email'],
                  recipient_list=['customer.support@brickfiesta.com', self.cleaned_data['email']],
                  fail_silently=False)
        pass
