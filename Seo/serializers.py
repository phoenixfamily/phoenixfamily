from rest_framework import serializers
from .models import SEOPage, Keyword


class SEOPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOPage
        fields = ['page_url', 'title', 'description', 'keywords']


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['name']
