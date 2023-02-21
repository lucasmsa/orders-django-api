from rest_framework import (
    viewsets,
    mixins
)
from core.models import Category
from category import serializers


class CategoryViewSet(mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('name')