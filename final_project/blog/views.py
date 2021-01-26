from django.http import HttpResponse

# Create your views here.
#main page
def index(request):
    return HttpResponse("Hello blogers!")