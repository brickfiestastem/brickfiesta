from django import forms
from django.core.mail import EmailMessage


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        str_message = "{}\nFrom {}".format(self.cleaned_data['message'],
                                           self.cleaned_data['name'])
        email = EmailMessage(
            subject="Brick Fiesta - Contact Us",
            body=str_message,
            from_email='customer.support@brickfiesta.com',
            to=['customer.support@brickfiesta.com'],
            cc=[self.cleaned_data['email']],
            reply_to=[self.cleaned_data['email']]
        )
        email.send()
        pass
