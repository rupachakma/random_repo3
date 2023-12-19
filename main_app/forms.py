from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField

from main_app.models import CustomUser, JobPost

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    user_type = forms.ChoiceField(label="Login as a :",choices=[("","..."),("Recruiter","Recruiter"),("Jobseeker","Jobseeker")],widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = CustomUser
        fields = ["username","email","display_name","user_type"]
        labels = {"email":'Email',"display_name":"Display Name"}
        widgets ={
            "email":forms.TextInput(attrs={'class':'form-control'}),
            "display_name":forms.TextInput(attrs={'class':'form-control'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(label="Username",widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=("Password"),widget=forms.PasswordInput(attrs={'class':'form-control'}))

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'openings', 'category', 'description', 'skill_set']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'openings': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'skill_set': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }


