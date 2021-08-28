from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from cutomer.models import *

class CreateNoteSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
class NoteSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"