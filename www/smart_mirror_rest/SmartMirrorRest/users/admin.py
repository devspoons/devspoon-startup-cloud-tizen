from django.contrib import admin
from .models import Users

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','password','image','level','register_date')

admin.site.register(Users, UsersAdmin)
