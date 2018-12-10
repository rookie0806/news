from . import models, serializers
from rest_framework.views import APIView
from rest_framework import status
from django.core.files import File
from django.db.models.functions import Length
from rest_framework.generics import ListAPIView
import requests
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.files.temp import NamedTemporaryFile
from datetime import datetime
from rookie.users import models as user_models
# Create your views here.


class getData(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            time = request.query_params.get('time', None)
            news_model = models.NewsPaper.objects.filter(date=time).order_by('Progress','Office_name')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.NewsPaperSerializer(news_model, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class getProgressWord(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            time = request.query_params.get('time', None)
            model = models.Word.objects.filter(date=time,Progress=True).order_by('-Count')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.WordPaperSerializer(model, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class getNotProgressWord(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            time = request.query_params.get('time', None)
            model = models.Word.objects.filter(date=time,Progress=False).order_by('-Count')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.WordPaperSerializer(model, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
