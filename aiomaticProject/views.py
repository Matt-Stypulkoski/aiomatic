from django.http import HttpResponse


def index(request):
	print('data is being loaded')
	return HttpResponse("Hello, world. Let's start our AI-o-matic project")


