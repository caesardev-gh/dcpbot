import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcpbot.settings")

django.setup()

from core import models
from django.conf import settings