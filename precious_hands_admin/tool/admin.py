from django.contrib import admin

from .models import Child, Donor, PaymentInterval, ImportedData, Title

# Register your models here.


admin.site.register(Child)
admin.site.register(Donor)
admin.site.register(PaymentInterval)
admin.site.register(ImportedData)
admin.site.register(Title)
