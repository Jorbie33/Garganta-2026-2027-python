from django.urls import path
from .views import user_list_create, user_detail_update_delete

urlpatterns = [
    path('users/', user_list_create, name='user-list-create'),
    path('users/<int:pk>/', user_detail_update_delete, name='user-detail-update-delete'),
]
