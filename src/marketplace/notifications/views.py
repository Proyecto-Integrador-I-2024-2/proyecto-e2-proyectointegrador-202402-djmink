from django.shortcuts import get_object_or_404,    render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from my_aplication.models import CompanyManager, Freelancer, User
from notifications.models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#@login_required
def notifications(request, id):
    # Busca el usuario base (User)
    user = get_object_or_404(User, id=id)

    # Determina si es Freelancer o CompanyManager
    try:
        p = Freelancer.objects.get(id=id)
        viewer_type = 'freelancer'
        notification_list = Notification.objects.filter(destiny=id)
        unread_notifications = notification_list.filter(read=False)
        profile_url = reverse('perfilFreelancer', args=[id])
        profile_image = p.image.url
        home_url = reverse('mainFreelancer', args=[id])
    except Freelancer.DoesNotExist:
        try:
            p = CompanyManager.objects.get(id=id)
            viewer_type = 'client'
            notification_list = Notification.objects.filter(destiny=id)
            unread_notifications = notification_list.filter(read=False)
            profile_url = reverse('perfilesCliente', args=[id])
            profile_image = p.image.url
            home_url = reverse('mainCliente', args=[id])
            
        except CompanyManager.DoesNotExist:
            # Si no es Freelancer ni CompanyManager
            viewer_type = 'unknown'
            notification_list = []
            unread_notifications = []
            profile_url = ''
            profile_image = ''
            home_url = ''
            id = ''

    # Contexto para el template
    context = {
        'p': p,
        'this_id': id,
        'profile_image': profile_image,
        'profile_url': profile_url,
        'notification_list': notification_list,
        'unread_notifications': unread_notifications,
        'viewer_type': viewer_type,
        'home_url': home_url,
        'at_home': False,
        'at_client_page': True,
        'at_projects_page': False,
    }

    return render(request, 'notifications.html', context)

@csrf_exempt
def mark_as_read(request, notification_id):
    if request.method == 'POST':
        try:
            # Buscar la notificación por ID
            notification = Notification.objects.get(id=notification_id)
            
            # Actualizar el atributo `read` a True
            notification.read = True
            notification.save()

            return JsonResponse({'success': True, 'message': 'Notification marked as read'})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Notification not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})