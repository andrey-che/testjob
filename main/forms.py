# -*- coding: utf-8 -*-
from django.forms import ModelForm
from main.models import dynModelList


class UsersForm(ModelForm):
    class Meta:
        model = dynModelList['users']


class RoomsForm(ModelForm):
    class Meta:
        model = dynModelList['rooms']
