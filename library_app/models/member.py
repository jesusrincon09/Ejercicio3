from django.db import models
from library_app.models.library import Library

class Member(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    membership_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    max_loans = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.library.name})"
