from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    BookViewSet, TicketViewSet, MessageViewSet, InternalNoteViewSet, CustomUserRegistration, UserView, EmailTokenObtainPairView
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'internal_notes', InternalNoteViewSet, basename='internal_note')

urlpatterns = [
    path('auth/register/', CustomUserRegistration.as_view(), name='register'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('', include(router.urls)),
]
