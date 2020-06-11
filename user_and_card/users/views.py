from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsOwner
from users import serializers


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [IsOwner()]

        return super().get_permissions()
