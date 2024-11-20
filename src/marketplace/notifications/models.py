#Django
from django.utils import timezone
from django.db import models
from django.dispatch import Signal
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.db.models.signals import post_save


from my_aplication.models import User

#Esta clase se encarga de acceder a las notificaciones en la base de datos filtrando por leidas y no leidas. 
class NotificationQuerySet(models.QuerySet):

    #Retorna las notificaciones leidas en el actual Queryset
    def read(self):
        return self.filter(read=True)
    
    #Retorna las notificaciones no leidas en el actual Queryset
    def unread(self):
        return self.filter(read=False)
        
    #Marca todas las notificaciones como leidas en el actual Queryset
    def mark_all_as_read(self, destiny=None):
        qs = self.read(False)
        
        if destiny:
            qs = qs.filter(destiny=destiny)
        
        return qs.update(read=True)
    
    #Marca todas las notificaciones como no leidas en el actual Queryset
    def mark_all_as_unread(self, destiny=None):
        qs = self.unread(False)

        if destiny:
            qs = qs.filter(destiny=destiny)
        
        return qs.update(read=False)

#Clase abstracta del gestor de notificaciones
class AbstractNotificationManager(models.Manager):

    def get_queryset(self):
        return self.NotificationQuerySet(self.Model, using=self._db)

#Clase abstracta de notificación
class AbstractNotification(models.Model):

    class Levels(models.TextChoices):
        sucess = 'Success', 'Success'
        info = 'Info', 'Info'
        wrong = 'Wrong', 'Wrong'

    level = models.CharField(choices=Levels.choices, max_length=20, default=Levels.info)

    destiny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)

    actor_content_type = models.ForeignKey(ContentType, related_name='notificate_actor', on_delete=models.CASCADE)
    actor_object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=220)

    read = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    objects = NotificationQuerySet.as_manager()
  
    class Meta:
        abstract = True

    def __str__(self):
        actor_name = self.actor.username if self.actor else "Unknown Actor"
        destiny_name = self.destiny.username if self.destiny else "Unknown Destiny"
        return f"Actor: {actor_name} -- Destiny: {destiny_name} -- Verb: {self.verb}"

#Clase de notificaciones
class Notification(AbstractNotification):
    
    class Meta(AbstractNotification.Meta):
        abstract = False

#Controlador para crear una instancia de notificación tras una llamada de señal de acción. 
def notify_signals(verb, **kwargs):
    destiny = kwargs.pop('destiny')
    actor = kwargs.pop('sender')

    public = bool(kwargs.pop('public', True))
    timestamp = kwargs.pop('timestamp', timezone.now())

    levels = kwargs.pop('level', Notification.Levels.info)

    if isinstance(destiny, Group):
        destinies = destiny.user_set.all()
    elif isinstance(destiny, (QuerySet, list)):
        destinies = destiny
    else:  
        destinies = [destiny]

    new_notification = []
    for destiny in destinies:
        notification = Notification(
            destiny = destiny,
            actor_content_type = ContentType.objects.get_for_model(actor),
            actor_object_id = actor.pk,
            verb = str(verb),
            public = public,
            timestamp = timestamp,
            level = levels,
        )
    
        notification.save()
        new_notification.append(notification)
    
    return new_notification


notificate = Signal()

notificate.connect(notify_signals, dispatch_uid='notificate.models.Notification')