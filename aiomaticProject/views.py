from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. Let's start our AI-o-matic project")
