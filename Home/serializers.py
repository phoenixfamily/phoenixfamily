from rest_framework import serializers
from .models import Content, Features, Vision


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = "__all__"


class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = "__all__"
