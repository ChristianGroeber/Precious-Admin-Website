from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Child, Donor, DonationPlan, Donation, MyUser
from django.contrib.auth.models import User


class CreateChild(forms.ModelForm):
    class Meta:
        model = Child
        fields = ('name', 'first_name', 'birthday', 'image')


class CreateDonor(forms.ModelForm):
    class Meta:
        model = Donor
        exclude = ()


class CreateDonationPlan(forms.ModelForm):
    class Meta:
        model = DonationPlan
        fields = ('donor', 'child', 'interval', 'amount', 'until')


class LoginUser(forms.ModelForm):
    class Meta:
        fields = ('name', 'password')


class CustomCreateUser(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class Donate(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donation_plan', 'date_donated')
