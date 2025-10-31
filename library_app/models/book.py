from django.db import models
from library_app.models.library import Library

class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.PROTECT, related_name='books')
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    published_year = models.PositiveIntegerField(blank=True, null=True)
    
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.author})"
