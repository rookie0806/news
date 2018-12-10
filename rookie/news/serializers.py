from rest_framework import serializers
from . import models
from rookie.users import models as user_models
from taggit_serializer.serializers import (TagListSerializerField,TaggitSerializer)

class NewsPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsPaper
        fields = (
            'Office_name',
            'Percentage',
            'Progress'
        )

class WordPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Word
        fields = (
            'Word',
            'Count',
        )