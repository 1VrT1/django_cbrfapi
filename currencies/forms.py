from django import forms

from .models import Currency


class CurrenciesForm(forms.Form):
    CHOICES = [
        (i.charcode, '{} ({})'.format(i.charcode, i.name)) for i in Currency.objects.all()
    ]
    date1 = forms.DateTimeField(input_formats=['%Y-%m-%d'],
                                widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '2020-02-20'}))
    date2 = forms.DateTimeField(input_formats=['%Y-%m-%d'],
                                widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '2020-02-20'}))
    currency = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
