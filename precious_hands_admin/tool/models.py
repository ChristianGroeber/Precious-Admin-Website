from django import forms
from django.db import models

# Create your models here.
from django.db.models import ForeignKey


class Child(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    birthday = models.DateField()
    image = models.ImageField(blank=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.name)


class Donor(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=300, default="")
    road = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    plz = models.CharField(max_length=4)
    city = models.CharField(max_length=50)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.name)


class PaymentInterval(models.Model):
    description = models.CharField(max_length=20)
    amount_months = models.IntegerField()

    def __str__(self):
        return self.description


class DonationPlan(models.Model):
    donor = ForeignKey(Donor, on_delete=models.CASCADE)
    child = ForeignKey(Child, on_delete=models.CASCADE)
    interval = ForeignKey(PaymentInterval, on_delete=models.CASCADE)
    amount = models.IntegerField()
    until = models.DateField()

    def __str__(self):
        return str(self.donor) + 'donates to ' + str(self.child) + ' ' + str(self.interval)


class Donation(models.Model):
    donation_plan = ForeignKey(DonationPlan, on_delete=models.CASCADE)
    date_donated = models.DateField()

    def __str__(self):
        return str(self.donation_plan.donor.first_name) + ' donated CHF ' + str(self.donation_plan.amount) + ' on the ' + str(self.date_donated)


class ImportedData(models.Model):
    import_data = models.FileField(upload_to='data/%D-%m-%Y')
