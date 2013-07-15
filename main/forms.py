# -*- coding: utf-8 -*-
from django.forms import ModelForm
from main.models import dynModelList

dynFormList = {}

for model in dynModelList:
    class Meta:
        model = dynModelList[model]

    formName = "modelForm_{0}".format(model)
    formData = {'Meta': Meta}
    dynFormList[formName] = type(formName, (ModelForm,), formData)
