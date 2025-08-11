from django.shortcuts import render
from django.utils.translation import get_language, get_language_bidi
from django.views.decorators.cache import cache_page
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework.views import APIView

from About.models import AboutUs
from Contact.forms import ContactForm
from Product.models import Product
from User.views import get_or_create_temporary_user, save_user_device_info, log_user_activity


@cache_page(60 * 15)
def contact(request):
    current_language = get_language()
    is_bidi = get_language_bidi()
    aboutUs = AboutUs.objects.first()
    products = Product.objects.all()

    if request.user.is_authenticated:
        user = request.user
    else:
        user = get_or_create_temporary_user(request)
        save_user_device_info(request, user)

    log = log_user_activity(request, request.build_absolute_uri(), user)

    return render(request, 'contact.html', {'LANGUAGE_CODE': current_language,
                                            'LANGUAGE_BIDI': is_bidi,
                                            'About': aboutUs,
                                            'Products': products,
                                            'activity_log_id': log.id,

                                            })


class EmailView(APIView):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.data, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            file = form.cleaned_data.get('file')

            email_subject = f"Message from {name}"
            email_body = f"Name: {name}\nPhone: {phone}\nEmail: {email}\n\nMessage:\n{message}"

            email_message = EmailMessage(
                email_subject,
                email_body,
                'customer@phoenixfamily.co',  # فرستنده
                ['info@phoenixfamily.co']  # گیرنده
            )

            if file:
                email_message.attach(file.name, file.read(), file.content_type)

            try:
                # Send the email
                email_message.send()
                return Response({"message": "Email successfully sent"}, status=200)
            except Exception as e:
                # Handle errors while sending the email
                return Response({"error": f"Error sending email: {str(e)}"}, status=500)

        return Response({"error": form.errors}, status=400)
