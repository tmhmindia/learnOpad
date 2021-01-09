from django.forms import ModelForm
from  facilitators.models import *
from myauth.models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from  LandingPage.models import *
from django.forms import ValidationError

# form of personal details 

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta: 
        model = CustomUser
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2' )
       
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Password must contain at least 8 character and should contain numbers and alphabet"
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password *'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email *'})
        self.fields['first_name'].widget.attrs.update({'placeholder':_('First Name *')})
        self.fields['last_name'].widget.attrs.update({'placeholder':_('Last Name *')})
        self.fields['password2'].widget.attrs.update({'placeholder':_('Confirm password *')})

    def save(self, commit = True): 
        user = super(UserForm, self).save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    def clean_password2(self):
        if self.cleaned_data['password2'] !=self.cleaned_data['password1']:
            raise forms.ValidationError("Confirm password was wrong !")
        return self.cleaned_data['password2']
    def clean(self):
        super(UserForm, self).clean() 
        email = self.cleaned_data['email']
       

        user=None
        try:
            user=CustomUser.objects.get(email=email)
        except:
            user=None
        if user:
            raise ValidationError("Email is already exist")
        return self.cleaned_data 

        
    
# Form of experience details  
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['Linkedin_Url', 'Website_Url', 'Youtube_Url','RExperience','TExperience']
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['Linkedin_Url'].widget.attrs.update({'placeholder': 'Linkedin Url *'})
        self.fields['Website_Url'].widget.attrs.update({'placeholder': 'Website Url'})
        self.fields['Youtube_Url'].widget.attrs.update({'placeholder': 'Youtube Url'})
        
#Form of query details
class FacilitatorQueriesForm(ModelForm):
    class Meta:
        model=FacilitatorQueries
        fields=('query',)
    def __init__(self, *args, **kwargs):
        super(FacilitatorQueriesForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({'placeholder': 'Ask Your Question(optional)','id':'autoresizing'})
