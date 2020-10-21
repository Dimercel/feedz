from django import forms
from django.forms import ModelForm

from .models import Category, Channel


class CreateChannelForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label=None)

    class Meta:
        model = Channel
        fields = ['url', 'name', 'post_limit', 'category']
