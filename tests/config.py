# -*- coding: utf-8 -*-
import os
from django.conf import settings, global_settings as parent


def configure():
    if settings.configured:
        return

    test_settings = {
        'DEBUG': True,
        'USE_TZ': True,
        'DATABASES': {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:"
            }
        },
        'INSTALLED_APPS': [
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "dynamicsites",
        ],
        'MIDDLEWARE_CLASSES': parent.MIDDLEWARE_CLASSES + (
            'dynamicsites.middleware.DynamicSitesMiddleware',
        ),
        'TEMPLATE_CONTEXT_PROCESSORS': parent.TEMPLATE_CONTEXT_PROCESSORS + (
            'dynamicsites.context_processors.current_site',
        ),
        'SITE_ID': 1,
        'NOSE_ARGS': ['-s'],
        'SITES_DIR': os.path.join(os.path.dirname(__file__), 'sites'),
        'DEFAULT_HOST': 'www.corp-umbrella-site.com',
        'HOSTNAME_REDIRECTS': {
            'aboutfood.com': 'www.about-food.com',
            'about-food.net': 'www.about-food.com',
            'meats.about-food.com': 'meat.about-food.com',
            'fruits.about-food.com': 'fruit.about-food.com',
            'vegetable.about-food.com': 'vegetables.about-food.com',
            'diary.about-food.com': 'dairy.about-food.com',
            'restaurant.about-food.com': 'restaurants.about-food.com',
            'dining.about-food.com': 'restaurants.about-food.com',
            'carnes.sobre-comida.com.br': 'carne.sobre-comida.com.br',
            'frutas.sobre-comida.com.br': 'fruta.sobre-comida.com.br',
            'legume.sobre-comida.com.br': 'legumes.sobre-comida.com.br',
            'leites.sobre-comida.com.br': 'leite.sobre-comida.com.br',
            'about-games.com': 'about.gam.es'
        }
    }
    settings.configure(**test_settings)
