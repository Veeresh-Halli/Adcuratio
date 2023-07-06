from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Blogs(models.Model):
    blog_id = models.UUIDField(default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    blog_image = models.ImageField(upload_to='static')

    def __str__(self):
        return self.title
    
    def get_details(self):
        details = {
            "blog_id" : self.blog_id,
            "author" : self.author.username,
            "title" : self.title,
            "description" : self.description,
            "blog_image" : self.blog_image.url
        }

        return details
