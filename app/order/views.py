from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Order
from order import serializers

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderDetailSerializer
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.OrderSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)