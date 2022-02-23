from django.contrib import admin
from banks.models import *

# Register your models here.
admin.site.register(Bank)
admin.site.register(Bank_account)
admin.site.register(Movement)
