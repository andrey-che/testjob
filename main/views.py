#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from main.models import dynModelList
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from forms import *
from main.forms import *
from django.forms.models import model_to_dict
from django.forms import ValidationError
from django.utils.translation import ugettext as _


def main(request):
    context = {}

    context['users'] = dynModelList['users'].objects.all()
    context['rooms'] = dynModelList['rooms'].objects.all()
    context['UsersForm'] = UsersForm()
    context['RoomsForm'] = RoomsForm()

    return render_to_response('main.html', context)


def xhr_getUsers(request):
    data = dynModelList['users'].objects.all()
    # Серилизация queryset'а
    data = serializers.serialize("json", data)

    data = json.dumps(data)
    return HttpResponse(data)


def xhr_getRooms(request):
    data = dynModelList['rooms'].objects.all()
    data = serializers.serialize("json", data)

    data = json.dumps(data)
    return HttpResponse(data)


def postForm(POST, Form):
    form = Form(POST or None)
    resp = {}

    if form.is_valid():
        resp['result'] = True
        resp['data'] = form.cleaned_data
        form.save()
    else:
        resp['result'] = False
        resp['errors'] = form.errors

    # Указана ф-ия для серилизации даты(datetime)
    data = json.dumps(resp, cls=DjangoJSONEncoder)
    return data


@csrf_exempt
def xhr_postUsers(request):
    if request.POST and request.is_ajax():
        data = postForm(request.POST, UsersForm)
        return HttpResponse(data)

    return HttpResponse("Not post!!!")


@csrf_exempt
def xhr_postRooms(request):
    if request.POST and request.is_ajax():
        data = postForm(request.POST, RoomsForm)
        return HttpResponse(data)

    return HttpResponse("Not post!!!")


def saveField(POST, modelName, Form):
    data = {}
    resp = {}

    # Загружаем данные редактируемого объекта
    try:
        model = dynModelList[modelName].objects.get(pk=POST.get('pk'))
        data = model_to_dict(model)
    except dynModelList[modelName].DoesNotExist:
        return HttpResponse("Not found!")

    # сохраняем старое значение
    oldValue = data.get(POST.get('field_name'))

    # Проверяем, есть ли такое поле вообще
    if POST.get('field_name') in data:
        # Заменяем отредактированное поле
        data[POST.get('field_name')] = POST.get('value')

        formRes = Form(data=data)

        if formRes.is_valid():
            resp['result'] = True

            # Редактирование объекта моделич через словарь данных
            model.__dict__.update(data)
            model.save()
        else:
            resp['result'] = False
            resp['errors'] = formRes.errors
            resp['oldValue'] = oldValue
    else:
        resp['result'] = False
        resp['oldValue'] = oldValue

    data = json.dumps(resp, cls=DjangoJSONEncoder)
    return data


@csrf_exempt
def xhr_editUsers(request):
    if request.POST and request.is_ajax():
        data = saveField(request.POST, 'users', UsersForm)
        return HttpResponse(data)

    return HttpResponse("not post!")


@csrf_exempt
def xhr_editRooms(request):
    if request.POST and request.is_ajax():
        data = saveField(request.POST, 'rooms', RoomsForm)
        return HttpResponse(data)

    return HttpResponse("not post!")

