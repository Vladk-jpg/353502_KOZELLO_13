from django.db import models
from accounts.models import UserProfile
from properties.models import Property

# Create your models here.

class Promo(models.Model):
    promo_code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    discount_percentage = models.PositiveIntegerField(verbose_name="Размер скидки (%)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    expires_at = models.DateTimeField(verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Promo"
        verbose_name_plural = "Promos"

    def __str__(self):
        return f"{self.promo_code} - {self.discount_percentage}%"

class Sale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    client = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_sales', verbose_name="Клиент")
    agent = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_sales', verbose_name="Агент")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='sales', verbose_name="Объект недвижимости")
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Промокод")
    sale_date = models.DateTimeField(verbose_name="Дата продажи", null=True, blank=True)
    contract_date = models.DateTimeField(verbose_name="Дата договора")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return f"Продажа {self.client} - {self.sale_date}"

    def get_final_price(self):
        """Calculate final price with discount if promo code is applied"""
        if self.promo:
            discount = self.property.price * (self.promo.discount_percentage / 100)
            return self.property.price - discount
        return self.property.price
