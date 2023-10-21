from django import forms
from prompt_toolkit.validation import ValidationError

from api.models import Tag, OperatorCodeModel, TimeZoneModel


class OperatorCodeForm(forms.Form):
    code = forms.IntegerField(label='Код оператора', widget=forms.TextInput(attrs={'type': 'number'}))


class TagForm(forms.Form):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))


class TimeZoneForm(forms.Form):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    timezone = forms.CharField(label='Зона(UTC+?)', widget=forms.TextInput(attrs={'class': 'form-control'}))

class ClientForm(forms.Form):
    phone_number = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    operator_code = forms.ModelChoiceField(
        queryset=OperatorCodeModel.objects.all(),
        label='Код',
        widget=forms.Select(attrs={'class': 'form-control'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='Таг',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    timezone = forms.ModelChoiceField(
        queryset=TimeZoneModel.objects.all(),
        label='Зона',
        widget=forms.Select(attrs={'class': 'form-control'}))


class MailingListForm(forms.Form):
    start_datetime = forms.DateTimeField(label='Начало', widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    end_datetime = forms.DateTimeField(label='Конец', widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    message = forms.CharField(label='Сообщение', widget=forms.TextInput(attrs={'class': 'form-control'}))
    operator_code = forms.ModelChoiceField(
        queryset=OperatorCodeModel.objects.all(),
        label='Код',
        widget=forms.Select(attrs={'class': 'form-control'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='Таг',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )


