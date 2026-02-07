from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdmin, IsSelfOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "destroy", "register"]:
            return [IsAdmin()]
        if self.action in ["retrieve", "update", "partial_update"]:
            return [IsSelfOrAdmin()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        url_name="register",
    )
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )
