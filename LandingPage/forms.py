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

class CorporateTalksForm(ModelForm):
    class Meta:
        model=CorporatesTalks
        fields=['name','email','mobile','company_name','training_need','message','city','state','check']
        widgets = {
            'training_need': forms.Select(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(CorporateTalksForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name','class':'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email','class':'form-control'})
        self.fields['mobile'].widget.attrs.update({'placeholder': 'Mobile Number','class':'form-control'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Query','class':'form-control'})
        self.fields['city'].widget.attrs.update({'placeholder': 'City','class':'form-control'})
        self.fields['state'].widget.attrs.update({'placeholder': 'State','class':'form-control'})
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Company Name','class':'form-control'})
    