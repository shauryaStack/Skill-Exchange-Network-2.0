import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'updated_skill_exchange_network.settings')
application = get_wsgi_application()
