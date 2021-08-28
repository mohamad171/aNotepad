from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    note = models.TextField()
    random_string = models.CharField(max_length=10)
    def link(self):
        return f"http://www.anotepad.ir/v/{self.random_string}"