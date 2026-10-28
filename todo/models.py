from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Task(models.Model):
    PRIMARY_CHOICES = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title =  models.CharField(max_length=150)
    priority = models.CharField(max_length=200,choices=PRIMARY_CHOICES,default='medium')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
