from django.contrib import admin
from . import models

@admin.register(models.NewsPaper)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'Office_name',
        'Percentage'
    )


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    list_display = (
        'Word',
        'Count',
        'Progress'
    )
