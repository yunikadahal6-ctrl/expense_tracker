from django.db import models
from django.contrib.auth.models import User  # <-- Yo naya import thapeko

# Create your models here.
class Bookmark(models.Model):
    CATEGORY_CHOICES = [
        ('work','Work'),
        ('study','Study'),
        ('entertainment','Entertainment'),
        ('other','Other')
    ]
    # Naya field thapeko: Yesle yo bookmark kun user ko ho vanera jodhcha
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    title = models.CharField(max_length=200)
    url = models.URLField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
    