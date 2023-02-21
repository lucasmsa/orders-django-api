from core.models import Category
from category.serializers import CategorySerializer
from rest_framework import serializers
from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)

    class Meta:
        model = Order
        fields = ['id', 'contact_name', 'contact_phone', 'real_state_agency', 'company', 'deadline', 'category']
        read_only_fields = ['id']

    def create(self, validated_data):
        category = validated_data.pop('category', {})
        category_object = Category.objects.get_or_create(name=category['name'])
        order = Order.objects.create(**validated_data, category=category_object[0])
        return order

    def update(self, instance, validated_data):
        category = validated_data.pop('category', None)

        if category is not None:
            category_object = Category.objects.get_or_create(name=category['name'])
            setattr(instance, 'category', category_object[0])

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        instance.save()
        return instance


class OrderDetailSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['description']