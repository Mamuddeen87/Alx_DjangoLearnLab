from django.apps import AppConfig

def ready(self):
    import relationship_app.signals  # ensures signals are loaded


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'
