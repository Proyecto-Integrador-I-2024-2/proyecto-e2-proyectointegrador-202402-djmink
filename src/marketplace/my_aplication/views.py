from django.shortcuts import render
from django.contrib import messages

def home(request):
    return render(request, 'my_aplication/first_page.html')


def home(request, id=None):
    if id == "accountDeleted":
        messages.success(request, 'Your account has been successfully deleted.')
    elif id == "accountDisabled":
        messages.success(request, 'Your account has been successfully disabled.')

    return render(request, 'my_aplication/first_page.html')
