#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from main.models import dynModelList
from main.forms import dynFormList
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.forms import ValidationError
from django.db.models.fields import DateField


def main(request):
    context = {}

    context['UsersForm'] = UsersForm()
    context['RoomsForm'] = RoomsForm()

    modelList = {}
    for modelName in dynModelList:
        modelData = {}
        modelFormName = "modelForm_{}".format(modelName)
        modelData = {"modelTitle": dynModelList[modelName]._meta.verbose_name.title(),
                     "modelFields": dynModelList[modelName]._meta.fields,
                     "modelForm": dynFormList[modelFormName]()
        }
        modelList[modelName] = modelData

    context['modelList'] = modelList

    return render_to_response('main.html', context)


@csrf_exempt
def xhr_getModel(request):
    modelName = request.GET.get("modelName")

    try:
        objsList = dynModelList[modelName].objects.all()
    except KeyError:
        return HttpResponse("Something wrong")

    # Серилизация queryset'а проходит не так как надо, в итоге в словаре поля не в нужном порядке, как в моделе, а
    # перемешаны
    #data = serializers.serialize("json", data)

    # Вот такой кастыль, зато в этом наборе данных есть инфа о типе поля.
    # В итоге возвращается список записей, каждый элемент списка - еще один список(полей) в виде словаря со всей инфой
    # о поле (имя, значение, тип)
    data = []
    for obj in objsList:
        dictObj = model_to_dict(obj)

        tmpList = []
        for field in obj._meta.fields:
            tmpDict = {}
            tmpDict['fieldName'] = field.name
            tmpDict['value'] = dictObj[field.name]
            tmpDict['fieldType'] = "DateField" if type(field) == DateField else "AnotherField"
            tmpList.append(tmpDict)

        data.append(tmpList)

    data = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(data)


@csrf_exempt
def xhr_editField(request):
    resp = {}
    try:
        formName = "modelForm_{}".format(request.POST['modelName'])
        pk = request.POST['pk']
        value = request.POST['value']
        fieldName = request.POST['fieldName']
        modelName = request.POST['modelName']

        form = dynFormList[formName]
    except KeyError:
        return HttpResponse("Editing error")

    # Загружаем данные редактируемого объекта
    try:
        model = dynModelList[modelName].objects.get(pk=pk)
        data = model_to_dict(model)
    except dynModelList[modelName].DoesNotExist:
        return HttpResponse("Editing error: not found!")

    # сохраняем старое значение
    oldValue = data.get(fieldName)

    # Проверяем, есть ли такое поле вообще
    if fieldName in data:
        # Заменяем отредактированное поле
        data[fieldName] = value

        formRes = form(data=data)

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
    return HttpResponse(data)


@csrf_exempt
def xhr_postRow(request):
    resp = {}
    try:
        modelName = request.POST['__modelName__']
        formName = "modelForm_{}".format(modelName)

        form = dynFormList[formName]
    except KeyError:
        return HttpResponse("Editing error")

    formRes = form(request.POST or None)

    if formRes.is_valid():
        resp['result'] = True
        resp['data'] = formRes.cleaned_data
        formRes.save()
    else:
        resp['result'] = False
        resp['errors'] = formRes.errors

    # Указана ф-ия для серилизации даты(datetime)
    data = json.dumps(resp, cls=DjangoJSONEncoder)
    return HttpResponse(data)

