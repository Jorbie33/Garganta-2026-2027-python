from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import BaseUser, Cart, CartProduct, Product, ProductTransaction, Transaction


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = BaseUser
        fields = ["username", "email", "password", "first_name", "middle_name", "last_name", "gender"]
        extra_kwargs = {"email": {"required": True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return BaseUser.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["id", "username", "email", "first_name", "middle_name", "last_name", "gender", "avatar"]
        read_only_fields = ["id", "username"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "sku", "price", "stock", "thumbnail", "created_at"]


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True), source="product", write_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ["id", "quantity", "product", "product_id", "subtotal"]

    def get_subtotal(self, obj):
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartProductSerializer(source="cart_products", many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total", "updated_at"]

    def get_total(self, obj):
        return sum(i.quantity * i.product.price for i in obj.cart_products.select_related("product"))


class ProductTransactionSerializer(serializers.ModelSerializer):
    item = ProductSerializer(read_only=True)

    class Meta:
        model = ProductTransaction
        fields = ["id", "quantity", "unit_price", "item"]


class TransactionSerializer(serializers.ModelSerializer):
    lines = ProductTransactionSerializer(source="product_transactions", many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["id", "created_at", "lines", "total"]

    def get_total(self, obj):
        return sum(l.quantity * l.unit_price for l in obj.product_transactions.all())
