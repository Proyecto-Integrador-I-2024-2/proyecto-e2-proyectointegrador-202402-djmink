from django.shortcuts import render

def home(request):
    return render(request, 'my_aplication/first_page.html')
