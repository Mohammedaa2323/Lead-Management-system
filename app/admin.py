from django.contrib import admin

from app.models import User,Task,Lead

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Lead)