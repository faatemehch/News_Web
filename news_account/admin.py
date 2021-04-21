from django.contrib import admin
from .models import UserInformation


# Register your models here.
class UserInformationAdmin( admin.ModelAdmin ):
    search_fields = ['__str__', 'education']


admin.site.register( UserInformation, UserInformationAdmin )
