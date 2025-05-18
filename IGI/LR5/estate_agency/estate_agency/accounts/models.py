from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from datetime import date

ROLE_CHOICES = (
    ('client', 'Клиент'),
    ('agent', 'Сотрудник'),
    ('admin', 'Администратор'),
)

phone_validator = RegexValidator(
    regex=r'^\+375\s\(?(17|25|29|33|44)\)?\s?\d{3}-\d{2}-\d{2}$',
    message="Телефон должен быть в формате: +375 (29) XXX-XX-XX"
)

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_validator], max_length=20)
    birth_date = models.DateField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='clients',
        blank=True,
        verbose_name='Клиенты'
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def age(self):
        return calculate_age(self.birth_date)

    def clean(self):
        # Проверка 18+
        if self.birth_date:
            if self.age() < 18:
                from django.core.exceptions import ValidationError
                raise ValidationError("Пользователю должно быть не менее 18 лет.")


class Staff(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='staff_profile')
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)
    position = models.CharField(max_length=100, verbose_name='Должность')
    experience = models.PositiveIntegerField(verbose_name='Опыт работы (лет)', default=0)
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"{self.user_profile.user.get_full_name() or self.user_profile.user.username} - {self.position}"

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
