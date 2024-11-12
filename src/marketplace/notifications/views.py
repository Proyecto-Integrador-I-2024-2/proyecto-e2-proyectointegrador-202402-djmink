from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView
from swapper import load_model


Notification = load_model('notifications', 'Notification')

class NotificationList(ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notification'

    #@method_decorator(login_required)
    #def dispatch(self, request, *args, **kwargs):
      #  return super(NotificationList, self).dispatch(request, *args, **kwargs)
    
    #def get_queryset(self):
     #   return self.request.user.notifications.all()