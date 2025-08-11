from urllib.parse import quote

from PhoenixFamily import settings
from .models import SEOPage
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str


def seo_context(request):
    path = request.path.strip("/")  # حذف اسلش اول و آخر
    seo_data = SEOPage.objects.prefetch_related('keywords').filter(page_url=f"/{path}/").first()

    if not seo_data:
        return {
            'seo_title': force_str(_(settings.SEO['default']['title'])),
            'seo_description': force_str(_(settings.SEO['default']['description'])),
            'seo_keywords': ", ".join([force_str(_(kw)) for kw in settings.SEO['default']['keywords']]),
        }

    return {
        'seo_title': seo_data.title,
        'seo_description': seo_data.description,
        'seo_keywords': ", ".join([kw.name for kw in seo_data.keywords.all()]),
        'canonical_url': quote(request.build_absolute_uri(), safe=':/')
    }
