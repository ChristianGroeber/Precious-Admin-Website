from django.contrib import admin

from tool.models import User, Child, Donor, PaymentInterval

# Register your models here.

admin.site.register(User)
admin.site.register(Child)
admin.site.register(Donor)
admin.site.register(PaymentInterval)