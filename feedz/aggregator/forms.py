import requests
from django import forms
from django.conf import settings
from django.core.validators import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Category, Channel


class CreateChannelForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label=None)

    class Meta:
        model = Channel
        fields = ['url', 'name', 'post_limit', 'category']

    def clean_url(self):
        data = self.cleaned_data
        resp = requests.get(data.get('url'), headers={
            'user-agent': settings.BOT_USER_AGENT
        })

        if resp.status_code != requests.codes.ok:
            raise ValidationError(
                _("Url return status %(status)s"),
                code='bad_request',
                params={'status': resp.status_code}
            )

        return data


class UpdateChannelForm(CreateChannelForm):
    class Meta:
        model = Channel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['last_seen'].disabled = True
        self.fields['last_sync'].disabled = True
