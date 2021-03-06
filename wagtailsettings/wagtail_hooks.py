from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from . import urls
from .permissions import user_can_edit_settings


def register_admin_urls():
    return [
        url(r'^settings/', include(urls)),
    ]
hooks.register('register_admin_urls', register_admin_urls)


def construct_main_menu(request, menu_items):
    if user_can_edit_settings(request.user):
        menu_items.append(MenuItem(
            _('Settings'),
            urlresolvers.reverse('wagtailsettings_index'),
            classnames='icon icon-cogs',
            order=1000
        ))
hooks.register('construct_main_menu', construct_main_menu)
