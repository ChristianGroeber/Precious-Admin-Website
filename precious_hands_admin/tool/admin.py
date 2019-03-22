from django.contrib import admin

from .models import Child, Donor, PaymentInterval

# Register your models here.


admin.site.register(Child)
admin.site.register(Donor)
admin.site.register(PaymentInterval)