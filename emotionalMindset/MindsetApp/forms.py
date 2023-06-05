from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, Contact
from django.contrib.auth.hashers import make_password
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username","email","password1","password2")
    def save(self,commit=True):
        user = super(NewUserForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name','email','password')
        widgets = {
            'password': forms.PasswordInput(),
        }  
    def save(self,commit=True):
        patient = super(PatientForm,self).save(commit=False)
        patient.password = make_password(self.cleaned_data['password'])
        if commit:
            patient.save()
        return patient
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name','email','message','phone')
    def save(self,commit=True):
        contact = super(ContactForm,self).save(commit=False)
        if commit:
            contact.save()
        return contact