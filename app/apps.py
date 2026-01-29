# Copyright (C) 2026 Ömer Rasim Sak
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
