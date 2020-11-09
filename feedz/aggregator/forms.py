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

    def clean_url(self):
        data = self.cleaned_data
        resp = requests.get(data.get('url'))

        if resp.status_code != requests.codes.ok:
            raise ValidationError(f"Url return status {resp.status_code}")

        return data['url']


class UpdateChannelForm(CreateChannelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label=None)

    class Meta:
        model = Channel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['last_seen'].disabled = True
        self.fields['last_sync'].disabled = True
