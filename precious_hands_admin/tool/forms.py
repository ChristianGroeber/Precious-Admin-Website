from django import forms
from .models import Child, Donor, DonationPlan, User


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
        model = User
        fields = ('name', 'password')
