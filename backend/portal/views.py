from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Book, Ticket, Message, InternalNote
from .serializers import (
    UserSerializer, UserCreateSerializer, BookSerializer, 
    TicketSerializer, MessageSerializer, InternalNoteSerializer,
    EmailTokenObtainPairSerializer
)
from .ai_services import process_new_ticket
from rest_framework_simplejwt.views import TokenObtainPairView

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class CustomUserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Book.objects.all()
        return Book.objects.filter(author=self.request.user)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Ticket.objects.all().order_by('-created_at')
        return Ticket.objects.filter(author=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Trigger AI Service right before saving
        description = self.request.data.get('description', '')
        # Cost Optimization: Send the user's email so the AI service only loads their specific books
        ai_data = process_new_ticket(description, author_email=self.request.user.email)
        
        serializer.save(
            author=self.request.user,
            category=ai_data.get('category', 'General'),
            priority=ai_data.get('priority', 'Medium'),
            ai_draft_response=ai_data.get('draft_response', '')
        )

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class InternalNoteViewSet(viewsets.ModelViewSet):
    serializer_class = InternalNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return InternalNote.objects.all()
        return InternalNote.objects.none()

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
