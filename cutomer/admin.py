from django.contrib import admin
from cutomer.models import *

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["id","link","user"]
