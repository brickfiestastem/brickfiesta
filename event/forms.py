from django import forms
from django.core.mail import send_mail
from django.core.mail import EmailMessage


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        str_from = "{} <{}>".format(self.cleaned_data['name'],
                                    self.cleaned_data['email'])
        email = EmailMessage(
            subject="Brick Fiesta - Contact Us",
            body=self.cleaned_data['message'],
            from_email=str_from,
            to=['customer.support@brickfiesta.com'],
            cc=[str_from],
            reply_to=['customer.support@brickfiesta.com',
                      str_from]
        )
        email.send()
        pass
