from django.db import models
import random

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    rd = random.randrange(1,50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.pk}]{self.title}"
    
    def get_absolute_url(self):
        return f"/blog/{self.pk}/"