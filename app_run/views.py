from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Run
from .serializers import RunSerializer, UserSerializer
from django.conf import settings

# Create your views here.
@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(details)


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.filter(is_superuser=False)  # Исключаем суперпользователей
        type = self.request.query_params.get('type')

        if type == 'coach':  # Если параметр равен 'coach', фильтруем по coach
            qs = qs.filter(is_staff=True)  # Фильтруем по is_staff=True, если параметр указан
        elif type == 'athlete':  # Если параметр равен 'athlete', фильтруем по athlete
            qs = qs.filter(is_staff=False)  # Фильтруем по is_staff=False, если параметр указан

        return qs
