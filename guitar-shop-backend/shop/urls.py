from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("auth/register/", views.RegisterView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/me/", views.MeView.as_view()),
    path("products/", views.ProductListView.as_view()),
    path("products/<int:pk>/", views.ProductDetailView.as_view()),
    path("cart/", views.CartView.as_view()),
    path("cart/items/", views.CartItemCreateView.as_view()),
    path("cart/items/<int:pk>/", views.CartItemDetailView.as_view()),
    path("checkout/", views.CheckoutView.as_view()),
    path("transactions/", views.TransactionListView.as_view()),
]
