import json
import uuid
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django_user_agents.utils import get_user_agent
from rest_framework import status
from rest_framework.generics import CreateAPIView

from .models import User, UserDeviceInfo, UserActivityLog
from django.contrib.auth import login, authenticate, get_user_model
from django.utils.crypto import get_random_string
from .serializers import RegisterSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.exceptions import NotFound


User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "Account created successfully.",
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "number": user.number,
            }
        }, status=status.HTTP_201_CREATED)

def get_or_create_temporary_user(request):
    if not request.session.get('user_id'):  # بررسی اینکه آیا کاربر موقت در سشن ذخیره شده است
        user = User.objects.create(
            id=uuid.uuid4(),
            first_name='Temporary',
            last_name=f'User-{get_random_string(6)}',
            is_temporary=True,
            is_active=True,
        )
        request.session['user_id'] = str(user.id)  # ذخیره شناسه کاربر در سشن

        login(request, user)  # لاگین کاربر موقت

        return user
    else:
        try:
            user = User.objects.get(id=request.session['user_id'], is_temporary=True)
            return user
        except User.DoesNotExist:
            # اگر کاربر وجود ندارد، باید مشکل را لاگ کرده و کاربر جدید ایجاد کنید
            del request.session['user_id']
            return get_or_create_temporary_user(request)


def get_device_info(request):
    user_agent = get_user_agent(request)
    ip_address = get_client_ip(request)

    return {
        'device_type': 'Mobile' if user_agent.is_mobile else 'Tablet' if user_agent.is_tablet else 'Desktop' if
        user_agent.is_pc else 'Unknown',
        'device_model': user_agent.device.family,
        'operating_system': user_agent.os.family,
        'os_version': user_agent.os.version_string,
        'browser': user_agent.browser.family,
        'browser_version': user_agent.browser.version_string,
        'ip_address': ip_address,
        'country': None,  # این بخش در مرحله بعد اضافه می‌شود
        'city': None,  # این بخش در مرحله بعد اضافه می‌شود
    }


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
    return ip


def save_user_device_info(request, user):
    if not UserDeviceInfo.objects.filter(user=user).exists():
        device_info = get_device_info(request)

        UserDeviceInfo.objects.create(
            user=user,
            device_type=device_info['device_type'],
            device_model=device_info['device_model'],
            operating_system=device_info['operating_system'],
            os_version=device_info['os_version'],
            browser=device_info['browser'],
            browser_version=device_info['browser_version'],
            ip_address=device_info['ip_address'],
            country=device_info['country'],
            city=device_info['city'],
        )


def log_user_activity(request, visited_page, user):
    # ثبت لاگ فعالیت
    activity_log = UserActivityLog.objects.create(
        user=user,
        visited_page=visited_page,
        entry_time=now(),
    )
    return activity_log


def log_exit_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        activity_log_id = data.get('activity_log_id')
        exit_time = data.get('exit_time')

        try:
            log = UserActivityLog.objects.get(id=activity_log_id)
            log.exit_time = exit_time
            log.save()
            return JsonResponse({'status': 'success'})
        except UserActivityLog.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Log not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


class UserCRUDView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "number"  # Use 'number' as the lookup field instead of 'pk'

    def get_object(self):
        """
        Override the default `get_object` method to look up users by `number`.
        """
        # Get the `number` from the URL kwargs
        number = self.kwargs.get('number')

        # Retrieve the user object or raise a 404 error if not found
        obj = get_object_or_404(User, number=number)

        return obj


@csrf_exempt
def login_view(request):
    # template = loader.get_template('login.html')
    # if request.user.is_authenticated:
    #     if request.user.is_staff:
    #         # ریدایرکت به داشبورد ادمین
    #         return redirect(f'/user/home/manager/{request.user.id}/')
    #
    #     elif request.user.is_admin:
    #         return redirect(f'/user/home/admin/{request.user.id}/')
    #
    #     else:
    #         # ریدایرکت به داشبورد کاربر عادی
    #         return redirect(f'/user/home/user/{request.user.id}/')
    # else:
    #     return HttpResponse(template.render(request))
    return render(request, 'login.html')


@csrf_exempt
def register_view(request):

    return render(request, 'register.html')


@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            number = data.get('username')  # دریافت شماره به عنوان username
            password = data.get('password')

            # اعتبارسنجی پسورد
            user = authenticate(request, username=number, password=password)
            if user is not None:
                login(request, user)
                user_data = {
                    'id': user.id,
                    'is_staff': user.is_staff,
                    'is_admin': user.is_admin,
                }
                return JsonResponse({'status': 'success', 'user': user_data}, status=200)
            else:
                return JsonResponse({'error': 'پسورد اشتباه است'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'error': 'نام کاربری وجود ندارد'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'فرمت JSON نامعتبر است'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
