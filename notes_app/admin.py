from django.contrib import admin
from .models import Note, Settings

# Register your models here.
admin.site.register(Note)
admin.site.register(Settings)