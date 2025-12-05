from django.contrib import admin
from .models import User, Company, JobSeeker
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass

admin.site.register(Company)
admin.site.register(JobSeeker)
