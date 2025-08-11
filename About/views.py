from django.shortcuts import render
from django.utils.translation import get_language, get_language_bidi
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from Product.models import Product
from User.views import get_or_create_temporary_user, save_user_device_info, log_user_activity
from .models import AboutUs, FAQ
from .serializers import AboutUsSerializer, FAQSerializer


@cache_page(60 * 15)
def about(request):
    current_language = get_language()
    is_bidi = get_language_bidi()
    aboutUs = AboutUs.objects.first()
    faq = FAQ.objects.all()
    products = Product.objects.all()

    if request.user.is_authenticated:
        user = request.user
    else:
        user = get_or_create_temporary_user(request)
        save_user_device_info(request, user)

    log = log_user_activity(request, request.build_absolute_uri(), user)

    return render(request, 'about.html', {'LANGUAGE_CODE': current_language,
                                          'LANGUAGE_BIDI': is_bidi,
                                          'About': aboutUs,
                                          'FAQ': faq,
                                          'Products': products,
                                          'activity_log_id': log.id,
                                          })


# _____________________________ Class Based Views for developing API ________________________________


class AboutUsView(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class FAQView(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
