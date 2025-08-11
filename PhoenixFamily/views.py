from django.http import HttpResponse


def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /

Sitemap: https://phoenixfamily.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
