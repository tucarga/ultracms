from django import template

from ultracore.models import Agency, Area, Service, Contact, MenuItem

register = template.Library()


def has_menu_children(page):
    if page.get_children().filter(live=True, show_in_menus=True):
        return True
    else:
        return False


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


@register.inclusion_tag('ultracore/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().filter(
        live=True,
        show_in_menus=True
    )
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.assignment_tag()
def get_menuitems():
    menuitems = MenuItem.objects.all()
    return menuitems


@register.inclusion_tag('ultracore/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.filter(
        live=True,
        show_in_menus=True
    )
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('ultracore/tags/secondary_menu.html', takes_context=True)
def secondary_menu(context, calling_page=None):
    pages = []
    if calling_page:
        root = context['request'].site.root_page
        parent = calling_page.get_parent()
        page = calling_page
        if parent == root:
            getter = page.get_siblings
        else:
            while parent != root:
                page = parent
                parent = page.get_parent()
            getter = page.get_children
        pages = getter().filter(
            live=True,
            show_in_menus=True
        )
    return {
        'pages': pages,
        # used to get active parent page
        'calling_page': calling_page.page_ptr,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('ultracore/tags/services.html', takes_context=True)
def services(context):
    return {
        'services': Service.objects.all(),
        'request': context['request'],
    }


@register.assignment_tag()
def get_contacts(page=None, area=None, agency=None):
    contacts = Contact.objects.all()
    if page is not None:
        tags = page.tags.all()
        contacts = contacts.filter(tags__in=tags)
    if area is not None:
        contacts = contacts.filter(area=area)
    if agency is not None:
        contacts = contacts.filter(agency=agency)

    return contacts


@register.assignment_tag(takes_context=True)
def get_agencies(context, filter=False):
    agencies = Agency.objects.all()
    agency = filter and context['request'].GET.get('agency')
    if agency:
        agencies = agencies.filter(name=agency)
    return agencies


@register.assignment_tag(takes_context=True)
def get_areas(context, filter=False):
    areas = Area.objects.all()
    area = filter and context['request'].GET.get('area')
    if area:
        areas = areas.filter(name=area)
    return areas
