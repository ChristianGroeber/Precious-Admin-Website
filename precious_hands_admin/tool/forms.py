from django import forms
from django.core.exceptions import ValidationError

from .models import Child, Donor, DonationPlan, Donation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateChild(forms.ModelForm):
    class Meta:
        model = Child
        fields = ('name', 'first_name', 'birthday', 'image')


class CreateDonor(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ('name', 'first_name', 'email_address', 'road', 'house_number', 'plz', 'city')


class CreateDonationPlan(forms.ModelForm):
    class Meta:
        model = DonationPlan
        fields = ('donor', 'child', 'interval', 'amount', 'until')


class LoginUser(forms.ModelForm):
    class Meta:
        fields = ('name', 'password')


class CreateUser(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def save(self, request, commit=True):
        print(str(self.cleaned_data['username']))
        User.save(
            request.user,
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.email
        )


class Donate(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('date_donated', )
