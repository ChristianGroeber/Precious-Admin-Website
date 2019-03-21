from django import forms
from django.db import models

# Create your models here.
from django.db.models import ForeignKey


class User(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=300, default="")
    password = models.CharField(max_length=200, default="1234")
    is_admin = models.BooleanField(default=False)


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
