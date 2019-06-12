from django import forms

from .models import Child, Donor, DonationPlan, Donation, ImportedData


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


class CreateUser(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)


class Donate(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('donation_plan', 'date_donated')


class ImportForm(forms.ModelForm):
    class Meta:
        model = ImportedData
        fields = ('import_data', )
