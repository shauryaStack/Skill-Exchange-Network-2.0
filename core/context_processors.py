from django.conf import settings
import json


def firebase_config(request):
    return {
        'firebase_config': settings.FIREBASE_CONFIG,
        'firebase_config_json': json.dumps(settings.FIREBASE_CONFIG),
    }
