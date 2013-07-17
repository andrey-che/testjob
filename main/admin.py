#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from main.models import dynModelList


# Регистрируем админку для всех моделей
for model in dynModelList:
    class Admin(admin.ModelAdmin):
        # Генерим список полей в моделе
        fieldList = []
        for field in dynModelList[model]._meta.fields:
            fieldList.append(field.name)

        list_display = fieldList

    admin.site.register(dynModelList[model], Admin)
