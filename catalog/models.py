from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils.text import slugify
from uuid import uuid4


# Create your models here.
class Catagory(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.CharField(
        unique=True, db_index=True, max_length=200, validators=[MinLengthValidator(3)]
    )

    class Meta:
        verbose_name_plural = "Catagories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, db_index=True)
    catagory = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField()
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    base_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if self.base_stock > 0:
            self.is_active = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
