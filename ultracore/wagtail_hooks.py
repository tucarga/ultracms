from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule

HALLO_PLUGINS = [
    'ultracore-hallojustify',
    'ultracore-hallocolorpicker',
    'ultracore-hallofontsize',
    'ultracore-hallofontfamily',
    'ultracore-hallofontcolor',
]

if settings.DEBUG:
    HALLO_PLUGINS.append('ultracore-hallohtml')


@hooks.register('insert_editor_js')
def editor_js():
    js_files = ['js/' + plugin + '.js' for plugin in HALLO_PLUGINS]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    script_head = '<script>'
    script_tail = '</script>'
    plugins = '\n'.join(
        'registerHalloPlugin("' + plugin + '");' for plugin in HALLO_PLUGINS
    )
    script = script_head + plugins + script_tail
    return js_includes + format_html(script)


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="' +
        settings.STATIC_URL +
        'css/font-awesome.min.css">')


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'span': attribute_rule({'style': True}),
        'font': attribute_rule({'size': True, 'face': True, 'color': True}),
        'p': attribute_rule({'align': True}),
    }
