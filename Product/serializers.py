from rest_framework import serializers
from .models import Product, Features


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = "__all__"
