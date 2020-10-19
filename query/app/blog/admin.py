from django.contrib import admin

# Register your models here.
from blog.models import ChildUser

admin.site.register(ChildUser)