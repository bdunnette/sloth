from django import forms

from .models import Skater


class SigninForm(forms.Form):
    skater = forms.ModelChoiceField(
        queryset=Skater.objects.filter(tags__name__in=["Active"]).order_by("name"),
        label="Select your name",
        empty_label="-- Select Skater --",
        widget=forms.Select(attrs={"class": "form-select form-select-lg"}),
    )
