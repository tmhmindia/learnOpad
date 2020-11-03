from django.forms import ModelForm,Textarea,ChoiceField
from django import forms
from  LandingPage.models import *

class ContactUsForm(ModelForm):
    class Meta:
        model=ContactUs
        fields=['name','email','categories','mobile','message']
        widgets = {
            'categories': forms.Select(attrs={'class':'custom-select'}),
        }
    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Your Name','class':'contact_input contact_input_name inpt'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your Email','class':'contact_input contact_input_email inpt'})
        self.fields['mobile'].widget.attrs.update({'placeholder': 'Your Mobile','class':'contact_input contact_input_subject inpt inpt'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Message','class':'contact_textarea contact_input inpt'})

