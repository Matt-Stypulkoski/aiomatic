from django.http import HttpResponse
from .api import create_trained_model


def index(request):
    print('data is being loaded')
    return HttpResponse("Hello, world. Let's start our AI-o-matic project")


def api(request):
    return create_trained_model(request)
