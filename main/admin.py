from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class StoreAdmin(admin.ModelAdmin):
    list_display = ('__str__','name', 'owner', 'date_created')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product)