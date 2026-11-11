"""Models follow the ERD: base_users, carts, cart_products, products,
transactions, product_transactions."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    middle_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    # username, email, password, first_name, last_name, is_active come from AbstractUser

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Cart(models.Model):
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk} ({self.owner})"


class CartProduct(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products")

    class Meta:
        unique_together = ("cart", "product")


class Transaction(models.Model):
    buyer = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="transactions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"


class ProductTransaction(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    item = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_transactions")
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="product_transactions"
    )
    # Price at time of purchase, so old orders keep their total if the price changes.
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
