from django.shortcuts import render
from django.views.generic.base import View
from .forms import CurrenciesForm
from .models import Currency

from xml.etree import ElementTree
import requests


class ChooseParams(View):
    """Формирование формы для того, чтобы пользователь заполнил даты и выбрал валюту для запроса"""
    def get(self, request):
        form = CurrenciesForm()
        return render(request, 'currencies/main.html', {'form': form})


class Info(View):
    def get_rate(self, date, currency):
        """Возвращает значение курса за определенную дату."""
        url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}/{}/{}'.format(date[-2:], date[5:7], date[:4])
        root, cnt = ElementTree.fromstring(requests.get(url).text), 0
        for element in root.iter("CharCode"):  # Пробегаемся по валютам поля CharCode
            if element.text == currency:  # И находим запрашиваемую валюту
                return float(root[cnt][4].text.replace(',', '.'))
            cnt += 1  # Для того, чтобы потом обратиться к нужной валюте и забрать значение

    def get(self, request):
        """Формирование словаря с нужными данными и вывод этих данных пользователю"""
        form = CurrenciesForm(request.GET)
        if form.is_valid():
            response = [i for i in request.GET.values()]
            try:  # Если пользователь введет некорректный год для валюты или несуществующую валюту.
                rate1, rate2 = self.get_rate(response[0], response[2]), self.get_rate(response[1], response[2])
                context = {
                    'date1': {'date': response[0], 'rate': rate1},  # Дата и курс валюты за эту дату
                    'date2': {'date': response[1], 'rate': rate2},
                    'difference': round((rate2 - rate1), 4),  # Разница курсов валют за выбранные даты.
                    'currency': Currency.objects.get(charcode=response[2])
                    }
            except TypeError:
                return render(request, 'currencies/info.html', {
                    'message': 'Произошла ошибка... Возможно дело в некорректной дате по отношению к валюте.'})

            return render(request, 'currencies/info.html', context)

        return render(request, 'currencies/info.html', {  # Если форма не пройдет валидацию.
            'message': 'Произошла ошибка... Проверьте правильность вводимых данных.'})
