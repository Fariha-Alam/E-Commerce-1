from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm


from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import Customer,Review

from django.contrib.auth.password_validation import validate_password

class SignUpForm(UserCreationForm):
     password1=forms.CharField(required=True,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}), help_text=password_validation.password_validators_help_text_html())
     password2=forms.CharField(required=True,label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
     email=forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}))
     class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        widgets={'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your name'})}
     def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        validate_password(password1, self.instance)  # Validate password complexity

        return cleaned_data



class LoginForm(AuthenticationForm):
   username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
   password = forms.CharField(label=("password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class passwordChange(PasswordChangeForm):
    old_password = forms.CharField(label=("old password"),strip=False,widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password',
      'class': 'form-control'}))
    new_password1 = forms.CharField(label=("New password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=("Confirm password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    

class passwordReset(PasswordResetForm):
    
    email=forms.EmailField(label=("Email"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))


class Mysetpassword(SetPasswordForm):
    new_password1 = forms.CharField(label=("New password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=("Confirm password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class': 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'locality', 'city', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }

              
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')

        if len(str(mobile)) != 11:
            raise forms.ValidationError('Please enter a valid 11-digit mobile number.')

        return mobile
class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('rating', 'comment')