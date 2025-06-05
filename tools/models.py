from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    UserID = models.CharField(max_length=100, primary_key=True)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    history = models.TextField(blank=True)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Histories(models.Model):
    HistoryID = models.AutoField(primary_key=True)
    MyApp_json = models.TextField()
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_histories')

    def __str__(self):
        return f"History {self.HistoryID} - User: {self.UserID}"

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Histories'

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    action_type = models.CharField(max_length=100)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'История действий'
        verbose_name_plural = 'История действий'

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.timestamp}"
