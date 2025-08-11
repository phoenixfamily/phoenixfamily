from django.shortcuts import render
from django.utils.translation import get_language, get_language_bidi
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from About.models import AboutUs
from User.views import get_or_create_temporary_user, save_user_device_info, log_user_activity
from .models import Product, Features
from .serializers import ProductSerializer, FeaturesSerializer


@cache_page(60 * 15)
def products(request, pk):
    current_language = get_language()
    is_bidi = get_language_bidi()
    aboutUs = AboutUs.objects.first()
    product = Product.objects.all()
    item = Product.objects.get(id=pk)
    features = Features.objects.filter(product_id=pk)

    if request.user.is_authenticated:
        user = request.user
    else:
        user = get_or_create_temporary_user(request)
        save_user_device_info(request, user)

    log = log_user_activity(request, request.build_absolute_uri(), user)

    return render(request, 'products.html', {'LANGUAGE_CODE': current_language,
                                             'LANGUAGE_BIDI': is_bidi,
                                             'About': aboutUs,
                                             'Products': product,
                                             'Item': item,
                                             'Features': features,
                                             'activity_log_id': log.id,

                                             })


# _____________________________ Class Based Views for developing API ________________________________

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FeaturesView(ModelViewSet):
    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
