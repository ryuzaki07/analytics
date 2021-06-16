import datetime

from django import forms

# input_formats=['%m-%d-%Y']


class DateForm(forms.Form):
    start_date = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Format: yyyy-m-d"}))
    end_date = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Format: yyyy-m-d"}))
