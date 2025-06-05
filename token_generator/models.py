from django.db import models
from django.contrib.auth.models import User
import secrets

class Token(models.Model):
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens', null=True, blank=True)

    @classmethod
    def generate_token(cls, user):
        """Generate a new token and save it to the database"""
        token = secrets.token_hex(32)  # 64 characters long
        return cls.objects.create(token=token, user=user)

    def __str__(self):
        return f"{self.token[:8]}... ({'Active' if self.is_active else 'Inactive'}) - {self.user.username if self.user else 'No user'}"

    class Meta:
        ordering = ['-created_at']
