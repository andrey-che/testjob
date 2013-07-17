#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from main.models import dynModelList
from django.db import models


class MainTest(TestCase):
    def check200(self, url, method="get", data={}):
        if method == "get":
            response = self.client.get(url, data)
        else:
            response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        return response

    # Ф-ия генерит словарь с именами полей данной модели и со значениями этих полей с учетом типа поля.
    def generateModelData(self, model):
        data = {}
        fields = dynModelList[model]._meta.fields
        # Генерим данные с учетом типа полей в моделе
        for field in fields:
            if field.name != "id":
                if type(field) == models.CharField:
                    data[field.name] = "Abcdefg123"
                elif type(field) == models.IntegerField:
                    data[field.name] = "123"
                elif type(field) == models.DateField:
                    data[field.name] = "2013-01-01"

        return data

    # Добавляем по одной записи в каждую модель
    def test_models(self):
        for model in dynModelList:
            data = self.generateModelData(model)
            # Создаем и сохраняем модель
            m = dynModelList[model](**data)
            m.save()

    def test_mainView(self):
        # Проверяем, что страница генерится без ошибок
        response = self.check200("/")

        # Проверяем, что список моделей не пуст
        self.assertNotEqual(response.context['modelList'], {})

    def test_getModelView(self):
        # Проверяем, что страница генерится без ошибок (без параметров)
        self.check200("/xhr_getModel/")

        # Проверяем, что страница генерится без ошибок (с запросом не существующей модели)
        self.check200("/xhr_getModel/", {"modelName": "jkesdbf*hyoew4j4'230'9"})

        # Проверяем, что страница генерится без ошибок (с запросом всех существующих моделей)
        for model in dynModelList:
            self.check200("/xhr_getModel/", {"modelName": dynModelList[model]})

    def test_editFieldView(self):
        # Проверяем, что страница генерится без ошибок (без параметров)
        self.check200("/xhr_editField/")

        # Проверяем, что страница генерится без ошибок (с некорректными параметрами)
        self.check200("/xhr_editField/", "post", {"pk": 123, "value": "0943jkdf -%^&", "fieldName": "ksdjkd",
                                                  "modelName": 983})

        # Пробуем редактировать все поля во всех моделях всеми типами данных(т.е. в некоторых случаях будут передаваться
        # некореектные данные)
        values = ["hdiujh", "2342", "2013-06-18"]
        # Для каждой модели
        for model in dynModelList:
            # Создаем для каждой модели запись
            data = self.generateModelData(model)
            m = dynModelList[model](**data)
            m.save()

            # И теперь пробуем редактировать все поля этой модели
            fields = dynModelList[model]._meta.fields
            # Для каждого поля
            for field in fields:
                # Для каждого типа данных, свой запрос
                for value in values:
                    self.check200("/xhr_editField/", "post", {"pk": 1, "value": value, "fieldName": field.name, "modelName": model})

    def test_postRowView(self):
        self.check200("/xhr_postRow/")
        self.check200("/xhr_postRow/", "post")

        # Для каждой моедли пробуем добавить запись
        for model in dynModelList:
            data = self.generateModelData(model)
            # Создаем и сохраняем модель
            self.check200("/xhr_postRow/", "post", data)

    def test_getLastRow(self):
         self.check200("/xhr_getLastRow/")

         # Пробуем получить последний итем для всех моделей
         for model in dynModelList:
             self.check200("/xhr_getLastRow/", {"modelName": dynModelList[model]})

