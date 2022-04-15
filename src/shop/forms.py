from django.forms import widgets
from  .models import Employee, Leave 
from django import forms
from  django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth.models import User
from django.core.exceptions import ValidationError  

class LeaveForm (forms.ModelForm):

    class Meta:
        model = Leave
        fields = ('start', 'end', 'reason')

        widgets={
            'start': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'reason':forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder': 'Give your reasons for a leave'}),
        }

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'mobile', 'address', 'gender', 'bank')

        widgets={
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control','placeholder': 'eg: 0712345678'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'bank':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'eg: Equity Bank'})
        }

class LeaveUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ('status',)
        widgets={
            'status':forms.Select(attrs={'class':'form-control'}),
        }

class EmployeeCreationForm(UserCreationForm): 
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username
    
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  

    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  

        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  