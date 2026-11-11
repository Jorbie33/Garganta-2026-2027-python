from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BaseUser, Cart, CartProduct, Product, ProductTransaction, Transaction
from .serializers import (
    CartProductSerializer,
    CartSerializer,
    ProductSerializer,
    RegisterSerializer,
    TransactionSerializer,
    UserSerializer,
)


def get_cart(user):
    """A user may have many carts (per the ERD); we always work with the newest one."""
    return user.carts.order_by("-id").first() or Cart.objects.create(owner=user)


# ---------- Auth ----------
class RegisterView(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []  # public: a stale token must not block sign-up
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ---------- Products ----------
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = []  
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search)
        ordering = self.request.query_params.get("ordering")
        if ordering in ("price", "-price", "name", "-created_at"):
            qs = qs.order_by(ordering)
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]


# ---------- Cart ----------
class CartView(APIView):
    def get(self, request):
        return Response(CartSerializer(get_cart(request.user)).data)


class CartItemCreateView(APIView):
    """Add a product. If it is already in the cart, the quantities add up."""

    def post(self, request):
        cart = get_cart(request.user)
        serializer = CartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        qty = max(int(serializer.validated_data.get("quantity", 1)), 1)
        item, _ = CartProduct.objects.get_or_create(cart=cart, product=product, defaults={"quantity": 0})
        item.quantity = min(item.quantity + qty, product.stock)
        if item.quantity < 1:
            item.delete()
            return Response({"detail": "This guitar is out of stock."}, status=400)
        item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    def _item(self, request, pk):
        return get_object_or_404(CartProduct, pk=pk, cart__owner=request.user)

    def patch(self, request, pk):
        item = self._item(request, pk)
        try:
            qty = int(request.data.get("quantity", item.quantity))
        except (TypeError, ValueError):
            return Response({"detail": "Quantity must be a number."}, status=400)
        if qty < 1:
            return Response({"detail": "Quantity must be at least 1."}, status=400)
        item.quantity = min(qty, item.product.stock)
        item.save()
        return Response(CartSerializer(item.cart).data)

    def delete(self, request, pk):
        item = self._item(request, pk)
        cart = item.cart
        item.delete()
        return Response(CartSerializer(cart).data)


# ---------- Checkout & orders ----------
class CheckoutView(APIView):
    @db_transaction.atomic
    def post(self, request):
        cart = get_cart(request.user)
        items = list(cart.cart_products.select_related("product"))
        if not items:
            return Response({"detail": "Your cart is empty."}, status=400)

        for item in items:
            if item.quantity > item.product.stock:
                return Response(
                    {"detail": f"Only {item.product.stock} of {item.product.name} left in stock."},
                    status=400,
                )

        order = Transaction.objects.create(buyer=request.user)
        for item in items:
            ProductTransaction.objects.create(
                transaction=order, item=item.product, quantity=item.quantity, unit_price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])
        cart.cart_products.all().delete()
        return Response(TransactionSerializer(order).data, status=status.HTTP_201_CREATED)


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user).prefetch_related(
            "product_transactions__item"
        )
