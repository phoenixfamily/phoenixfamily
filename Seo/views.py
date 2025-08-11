from rest_framework import viewsets
from django.http import HttpResponse
from Seo.models import SEOPage, Keyword
from Seo.serializers import SEOPageSerializer, KeyWordSerializer


class SEOPageView(viewsets.ModelViewSet):
    queryset = SEOPage.objects.all()
    serializer_class = SEOPageSerializer


class KeywordView(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeyWordSerializer


def test_path(request):
    return HttpResponse(f"Request Path: {request.path}")
