from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..models import User
from ..serializers.admin_serializer import UserAdminSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]
