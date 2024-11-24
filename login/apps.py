from django.apps import AppConfig
from django.conf import settings

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

    def ready(self):
        # aqui se hace una importancion ya que se necesita que cargue la aplicacion
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save
        
        def add_to_default_group(sender, **kwargs):
            user = kwargs['instance']
            if kwargs['created']:
                group, ok = Group.objects.get_or_create(name='estudiante')
                group.user_set.add(user)
                
        post_save.connect(add_to_default_group,
                            sender=settings.AUTH_USER_MODEL)