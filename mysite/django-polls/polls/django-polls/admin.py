# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.contrib import admin
from polls.models import Choice,Question
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text']
    fieldsets = [
            (None, {'fields': ['question_text']}),
            ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)
