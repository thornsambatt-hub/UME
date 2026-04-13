from django.db import models
from django.contrib.auth.hashers import check_password, identify_hasher, make_password
from django.core.exceptions import ValidationError


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    license = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "manufacturer"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class User(models.Model):
    ROLE_ADMIN = "Admin"
    ROLE_USER = "User"
    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_USER, "User"),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ROLE_USER)
    remark = models.TextField(blank=True)
    is_disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def clean(self):
        super().clean()
        if self.is_disabled and self.role == self.ROLE_ADMIN:
            raise ValidationError("Disabled users cannot keep the Admin role.")

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        if not self.password:
            return False

        try:
            identify_hasher(self.password)
        except ValueError:
            return self.password == raw_password

        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if self.password:
            try:
                identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.FloatField()
    made_at_date = models.DateTimeField(db_column="madeAtDate")
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="products",
    )
    expiration_date = models.DateTimeField(db_column="expirationDate")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    qty = models.IntegerField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stocks"

    def __str__(self):
        return f"{self.product.name} ({self.qty})"
