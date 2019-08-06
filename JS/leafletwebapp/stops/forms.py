from django import forms
from .models import Stops
from stops.models import post


class StopsForm(forms.ModelForm):
    post = forms.CharField()
    class Meta:
        model = post
        fields = ('post',)