from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from api.models import ClientModel, MessageModel, MailingListModel, Tag, OperatorCodeModel, TimeZoneModel
# from .models import CustomUser
from django_mailing.forms import ClientForm, MailingListForm, TagForm, OperatorCodeForm, TimeZoneForm
from django.contrib.auth.forms import UserCreationForm
import pika
from django.conf import settings
import requests
import logging


logger = logging.getLogger(__name__)


def check_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        connection.close()
        return True
    except pika.exceptions.AMQPError:
        return False


def index(request):
    if check_rabbitmq_connection():
        # сли подключение к RabbitMQ установлено успешно
        success = 'Успешное подключение к rebbitMQ'
        return render(request, 'index.html', {'success': success})
    else:
        # если подключение к RabbitMQ не установлено
        return HttpResponse("Failed to connect to RabbitMQ")


def operator_code(request):
    if request.method == "POST":
        form = OperatorCodeForm(request.POST)
        if form.is_valid():
            operator_code = OperatorCodeModel(
                code=form.cleaned_data['code']
            )
            operator_code.save()
    else:
        form = OperatorCodeForm()
    operator_cods = OperatorCodeModel.objects.all()
    return render(request, 'operator_code.html', {'operator_cods': operator_cods, 'form': form})


def operator_code_delete(request, code_id):
    code = get_object_or_404(OperatorCodeModel, id=code_id)
    if request.method == "POST":
        code.delete()
    return redirect('operator_cods')


def tags_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = Tag(
                name=form.cleaned_data['name']
            )
            tag.save()
            return redirect('tags')
    else:
        form = TagForm()
    tags = Tag.objects.all()
    return render(request, 'tags.html', {'tags': tags, 'form': form})


def tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        tag.delete()
    return redirect('tags')


def timezone_view(request):
    if request.method == 'POST':
        form = TimeZoneForm(request.POST)
        if form.is_valid():
            timezone = TimeZoneModel(
                name=form.cleaned_data['name'],
                timezone=form.cleaned_data['timezone']
            )
            timezone.save()
            return redirect('timezone')
    else:
        form = TimeZoneForm()
    timezone = TimeZoneModel.objects.all()
    return render(request, 'timezone.html', {'timezone': timezone, 'form': form})


def timezone_delete(request, timezone_id):
    timezone = get_object_or_404(TimeZoneModel, id=timezone_id)
    if request.method == 'POST':
        timezone.delete()
    return redirect('timezone')


def messages_view(request):
    messages = MessageModel.objects.all()
    return render(request, 'messages.html', {'messages': messages})


class MailingUpdateView(UpdateView):
    model = MailingListModel
    fields = ['start_datetime', 'end_datetime', 'message', 'operator_code', 'tags']
    template_name = 'edit_mailing_data.html'
    success_url = '/mailing_list/'


def mailing_list_view(request):
    current_time = timezone.localtime(timezone.now())
    if request.method == 'POST':
        form = MailingListForm(request.POST)
        if form.is_valid():
            # Создайте объект MailingListModel и сохраните его в базе данных
            mailing = MailingListModel(
                start_datetime=form.cleaned_data['start_datetime'],
                end_datetime=form.cleaned_data['end_datetime'],
                message=form.cleaned_data['message'],
                operator_code=form.cleaned_data['operator_code'],
            )
            mailing.save()

            # Теперь вы можете добавить теги к объекту mailing
            tags = form.cleaned_data.get('tags')
            if tags:
                if isinstance(tags, Tag):  # Проверяем, является ли tags объектом Tag
                    tags = [tags]  # Преобразуем tags в список, если это одиночный объект
                mailing.tags.set(tags)  # Присвойте теги объекту mailing
            logger.info(f'Рассылка "{mailing.message}" создана id: {mailing.id}')
            # Возвращение редиректа
            return redirect('mailing_list')

    else:
        form = MailingListForm

    mailings = MailingListModel.objects.all()
    return render(request, 'mailing_list.html', {'mailings': mailings, 'form': form})


def client_list_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = ClientModel(
                phone_number=form.cleaned_data['phone_number'],
                operator_code=form.cleaned_data['operator_code'],
                timezone=form.cleaned_data['timezone']
            )
            client.save()
            logger.info(f'Клиент "{client.phone_number}" создан id: {client.id}')
            tags = form.cleaned_data.get('tags')
            if tags:
                if isinstance(tags, Tag):  # Проверяем, является ли tags объектом Tag
                    tags = [tags]  # Преобразуем tags в список, если это одиночный объект

                client.tags.set(tags)  # Установите связи с выбранными тегами
            return redirect('client')
    else:
        form = ClientForm()

    clients = ClientModel.objects.all()
    return render(request, 'client.html', {'clients': clients, 'form': form})


class ClientUpdateView(UpdateView):
    model = ClientModel
    fields = ['phone_number', 'operator_code', 'tags', 'timezone']
    template_name = 'edit_client_data.html'
    success_url = '/client/'

    def form_valid(self, form):
        # Получаю id клиента из объекта, который будет обновлен
        client_id = self.object.id

        logger.info(f'Обновление данных клиента с id: {client_id}')

        return super().form_valid(form)


def delet_client(request, client_id):
    client = ClientModel.objects.get(id=client_id)
    if request.method == 'POST':
        logger.info(f'Удаление клиента с id: {client.id}')
        client.delete()
    return redirect('client')


def delete_mailing(request, mailing_id):
    mailing = MailingListModel.objects.get(id=mailing_id)
    if request.method == "POST":
        logger.info(f'Удаление рассылки с id: {mailing.id}')
        mailing.delete()
    return redirect('mailing_list')


class MailingLoginView(LoginView):
    template_name = 'auth/login.html'


class MailingLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'auth/logout.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'auth/register_user.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def login_github(request):
    print('start -> login_github')
    client_id = settings.GITHUB_CLIENT_ID
    scope = 'read:user'
    state = 'somerandomstring123'  # to prevent csrf
    return redirect(
        'https://github.com/login/oauth/authorize?client_id={}&scope={}&state={}'.format(client_id,
                                                                                         scope, state,
                                                                                         ))
def login_github_callback(request):
    print('start -> login_github_callback')
    code = request.GET.get('code', None)
    print(code, 'Что то принтую')
    if not code:
        return redirect(reverse("index", args=(), kwargs={}))

    params = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_SECRET,
        'code': code,
        'Content-Type': 'application/json'
    }

    headers = {
        'Accept': 'application/json'
    }

    result = requests.post('https://github.com/login/oauth/access_token', data=params, headers=headers)
    # print(result)
    # print(result.text)
    # print(result.json())
    token = result.json().get('access_token')
    user_api_url = 'https://api.github.com/user'
    headers = {
        'Authorization': 'token ' + token,
        'Accept': 'application/json'
    }
    result = requests.get(user_api_url, headers=headers)
    # print(result.json())
    user_data = result.json()
    username = user_data.get('login', None)
    print(username)
    if not username:
        print('username not present in data received from github {}')
        return redirect(reverse("index", args=(), kwargs={}))

    try:
        user = User.objects.get(username=username)  # проверка по email, что пользователь уже есть в БД
        print('user already in db')
    except User.DoesNotExist as e:
        print(f'Error_1: {e}')

        # Если пользователя нет в БД => Создание нового пользователя
        try:
            print('start create new User')
            user = User()
            user.username = user_data.get('login', None)
            user.email = user_data.get('email', None)
            user.is_admin = False
            user.is_active = True
            user.is_superuser = False

            user.save()
            print('user created in db')
        except Exception as e:
            print(f'login error: {e}')

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    print('Login by GITHUB Success')
    return redirect(reverse("index", args=(), kwargs={}))
