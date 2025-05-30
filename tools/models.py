from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Модель пользователя (расширяем стандартную модель Django)
class CustomUser(AbstractUser):
    # Дополнительные поля, если нужны
    # Например, телефон, дата рождения и т.д.
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return self.username


# 2. Модель истории действий пользователя
class History(models.Model):
    user = models.ForeignKey(
        "CustomUser",  # Связь с пользователем
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="histories"  # Удобный доступ через user.histories.all()
    )
    
    action = models.TextField(
        verbose_name="Действие",
        help_text="Описание действия пользователя"
    )
    
    timestamp = models.DateTimeField(
        verbose_name="Дата и время",
        auto_now_add=True
    )
    
    # Пример дополнительного поля для структурированных данных
    metadata = models.JSONField(
        verbose_name="Дополнительные данные",
        null=True,
        blank=True,
        default=dict,
        help_text="JSON-данные о действии"
    )

    class Meta:
        verbose_name = "История действий"
        verbose_name_plural = "История действий"
        ordering = ["-timestamp"]  # Сортировка по убыванию даты
    
    def __str__(self):
        return f"{self.user} - {self.action[:30]}..."