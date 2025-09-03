from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Property(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("reserved", "Reserved"),
    ]
    title = models.CharField(max_length=100, verbose_name="Title")
    price = models.IntegerField(verbose_name="Price", validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, verbose_name="Description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name="Category")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Created At")

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('property_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title} ({self.price} BYN)"
