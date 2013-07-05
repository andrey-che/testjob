#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib import admin
import yaml

def generateModel(name, rawModel):
    class Meta:
        pass
        if rawModel['title']:
            verbose_name = rawModel['title']
            verbose_name_plural = rawModel['title']

    fields = {
        '__module__': __name__,
        'Meta': Meta,
    }

    fieldsList = []

    for field in rawModel['fields']:
        if field['type'] == 'char':
            fields[field['id']] = models.CharField(field['title'], max_length=255)
            fieldsList.append(field['id'])
        elif field['type'] == 'int':
            fields[field['id']] = models.IntegerField(field['title'])
            fieldsList.append(field['id'])
        elif field['type'] == 'date':
            fields[field['id']] = models.DateField(field['title'])
            fieldsList.append(field['id'])

    model = type(name, (models.Model,), fields)

    # Registering admin panel
    class Admin(admin.ModelAdmin):
        list_display = fieldsList

    admin.site.register(model, Admin)

    return model

# Reading config
fd = open(settings.DB_CONFIG)
rawDB = yaml.load(fd)
fd.close()

dynModelList = {}

# Generating models
for name in rawDB:
    dynModelList[name] = generateModel(name, rawDB[name])

