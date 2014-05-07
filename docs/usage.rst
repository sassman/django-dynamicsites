========
Usage
========

Before you install django-dynamicsites, make sure you have configured at
 least 1 site in the admin panel, because once django-dynamicsites is
 installed, it will try to lookup a site from request.get_host(), and
 if none exists it will always throw 404

Configuration
-------------

1. Add the app to INSTALLED_APPS ::

        INSTALLED_APPS = (
            ...
            'dynamicsites',
        )

2. Add the middleware to MIDDLEWARE_CLASSES ::

        MIDDLEWARE_CLASSES = (
            ...
            'dynamicsites.middleware.DynamicSitesMiddleware'
        )

3. Add the context processor to TEMPLATE_CONTEXT_PROCESSORS ::

        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            'dynamicsites.context_processors.current_site',
        )

4. Configure dynamicsites by adding SITES_DIR, DEFAULT_HOST, and HOSTNAME_REDIRECTS to settings.py ::

        SITES_DIR = os.path.join(os.path.dirname(__file__), 'sites')
        DEFAULT_HOST = 'www.your-default-site.com'
        HOSTNAME_REDIRECTS = {
            'redirect-src-1.com':         'www.redirect-dest-1.com',
            ...
        }

5. If your local environment (eg. test, dev, staging) uses different hostnames than production, set the ENV_HOSTNAMES map as well ::

        ENV_HOSTNAMES = {
            'my-site.dev':    'www.your-default-site.com',
            ...
        }

6. make ``sites`` dir (from the SITES_DIR setting above) and put a ``__init__.py`` file inside

7. make a site dir for each site you're hosting (eg. ``mkdir sites/{{mysyte}}``) <-- you'll put ``{{mysyte}}`` in the admin screen when you go to configure mysyte there.  Make sure to put an ``__init__.py`` file in each site dir as well.

8. run ``syncdb``.  If your django_site table fails to modify, you will need to modify the table via sql::

        alter table django_site add column folder_name varchar(255);
        alter table django_site add column subdomains varchar(255);

9. go to the admin panel for sites.  You should see two fields added now, one for the site folder name (#8 above) and another for which subdomains you wish to support


Debugging
---------

In the current codebase, if you have the django debug toolbar installed and want enable redirect tracking, ie.::

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': True,
    }

django-dynamicsites will intercept redirects, which is very helpful when dialing in your site config.

There's also a view included with the codebase which is useful for checking which site dynamicsites thinks you're seeing.  Just add an entry to your urls.py file::

    from dynamicsites.views import site_info

    urlpatterns += patterns('',
        url(r'^site-info/$', site_info),
    )

Notes
-----

* you need to run syncdb after dynamicsites is installed (to be sure the fields folder_name and subdomains is added to the standard Site model)
* in sites folder and each sub folder must have a __init__.py file (except the templates folder)

Settings Keys Explained
-----------------------

::

    SITES_MODULE = 'module.where.sites.live'

- default value: ``''``

- purpose: define where the sites/* folder exists that are used for subdomain specific overwrites. Such as urls.py etc.

- when to set: only needed if your ``sites`` folder does not live in your django root dir



