# Copyright (C) 2026 Ömer Rasim Sak
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
ASGI config for OpenStadtBank project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpenStadtBank.settings')

application = get_asgi_application()
