from django.db import models
from django.contrib.auth.models import User
import random
import string

class Password(models.Model):
    password = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords', null=True, blank=True)
    # Для истории можно добавить параметры генерации, если нужно

    @classmethod
    def generate_password(cls, user, length=12, use_lower=True, use_upper=True, use_digits=True, use_special=True):
        """Генерирует новый пароль по выбранным параметрам и сохраняет его в базе"""
        chars = ''
        if use_lower:
            chars += string.ascii_lowercase
        if use_upper:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += '!@#$%^&*()-_=+[]{}|;:,.<>?/'
        if not chars:
            chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for _ in range(length))
        return cls.objects.create(password=password, user=user)

    def __str__(self):
        return f"{self.password[:8]}... ({'Active' if self.is_active else 'Inactive'}) - {self.user.username if self.user else 'No user'}"

    class Meta:
        ordering = ['-created_at']
