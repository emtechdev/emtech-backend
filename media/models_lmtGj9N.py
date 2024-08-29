from django.db import models
from django.contrib.auth.models import User



class Room(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)

    def __str__(self): 
        return self.name
    
class Task(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    arabic_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='tasks/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Assign(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    done_at = models.DateTimeField(auto_now_add=True)
    supervisor_approved = models.BooleanField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)



    def __str__(self):
        return self.user.username