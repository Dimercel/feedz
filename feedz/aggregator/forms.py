import requests
from django import forms
from django.core.validators import ValidationError
from django.forms import ModelForm

from .models import Category, Channel


class CreateChannelForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label=None)

    class Meta:
        model = Channel
        fields = ['url', 'name', 'post_limit', 'category']

    def clean(self):
        cleaned_data = super(CreateChannelForm, self).clean()
        resp = requests.get(cleaned_data.get('url'))

        if resp.status_code != requests.codes.ok:
            raise ValidationError(f"Url return status {resp.status_code}")

        return cleaned_data
