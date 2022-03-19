from django.contrib import admin
from banks.models import *

# Register your models here.
admin.site.register(Bank)
admin.site.register(Account_type)
admin.site.register(Bank_account)
admin.site.register(Movement_type)
admin.site.register(Movement)

