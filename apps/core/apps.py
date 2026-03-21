from django.apps import AppConfig


class CoreConfig(AppConfig):


    #like setting but only for this app, used for configuration and initialization of the app

    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    name = 'apps.core'
