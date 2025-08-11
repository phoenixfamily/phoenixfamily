from django.db.models import Q
from django.utils.translation import get_language
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from About.models import AboutUs
from Blog.models import BlogPost
from Blog.serializers import BlogPostSerializer
from Product.models import Product


# لیست مقالات
class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blogs.html"
    context_object_name = "blog_posts"
    paginate_by = 10  # تعداد مقالات در هر صفحه

    def get_queryset(self):
        queryset = BlogPost.objects.all().order_by("-published_date")
        filters = Q()
        author = self.request.GET.get("author")
        search = self.request.GET.get("search")

        if author:
            filters &= Q(author__username__icontains=author)
        if search:
            filters &= Q(title__icontains=search)

        return queryset.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = BlogPost.objects.count()  # تعداد کل مقالات
        context['About'] = AboutUs.objects.first()
        context['products'] = Product.objects.all()

        return context


# جزئیات مقاله
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blogpost.html"
    context_object_name = "blog_post"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(BlogPost, id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = get_language()  # زبان جاری را اضافه می‌کنیم

        page_title = self.get_page_title()  # عنوان صفحه
        page_content = self.get_page_content()  # توصیف صفحه
        page_image = self.get_page_image()

        meta_title = self.get_meta_title()  # عنوان صفحه
        meta_description = self.get_meta_description()  # توصیف صفحه
        meta_keywords = self.get_meta_keywords()  # کلمات کلیدی
        canonical_url = self.request.build_absolute_uri(self.request.path)

        context['page_title'] = page_title
        context['page_content'] = page_content
        context['page_image'] = page_image

        context['meta_title'] = meta_title
        context['meta_description'] = meta_description
        context['meta_keywords'] = meta_keywords
        context['canonical_url'] = canonical_url

        return context

    def get_page_title(self):
        # شما می‌توانید عنوان صفحه را بر اساس عنوان مقاله بسازید
        blog_post = self.get_object()
        return blog_post.title

    def get_page_content(self):
        # توصیف صفحه می‌تواند از محتوای مقاله گرفته شود
        blog_post = self.get_object()
        return blog_post.content  # یا هر فیلدی که توصیف کوتاهی از مقاله باشد

    def get_page_image(self):
        # کلمات کلیدی می‌تواند بر اساس دسته‌بندی یا برچسب‌های مقاله باشد
        blog_post = self.get_object()
        return blog_post.image  # اگر مقاله دسته‌بندی‌ها داشته باشد

    def get_meta_title(self):
        # شما می‌توانید عنوان صفحه را بر اساس عنوان مقاله بسازید
        blog_post = self.get_object()
        return blog_post.meta_title

    def get_meta_description(self):
        # توصیف صفحه می‌تواند از محتوای مقاله گرفته شود
        blog_post = self.get_object()
        return blog_post.meta_description  # یا هر فیلدی که توصیف کوتاهی از مقاله باشد

    def get_meta_keywords(self):
        # کلمات کلیدی می‌تواند بر اساس دسته‌بندی یا برچسب‌های مقاله باشد
        blog_post = self.get_object()
        return blog_post.meta_keywords  # اگر مقاله دسته‌بندی‌ها داشته باشد


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-published_date')  # لیست مقالات مرتب‌شده بر اساس تاریخ انتشار
    serializer_class = BlogPostSerializer
