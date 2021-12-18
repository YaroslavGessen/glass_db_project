from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}

    return render(request, 'app/home.html', context)


def about_page(request):
    return render(request, 'app/about.html', {'title': 'About'})