from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/ultracore-hallojustify.js',
        'js/ultracore-hallocolorpicker.js',
        'js/ultracore-hallofontsize.js',
        'js/ultracore-hallofontfamily.js',
        'js/ultracore-hallofontcolor.js',
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
        registerHalloPlugin('ultracore-hallojustify');
        registerHalloPlugin('ultracore-hallocolorpicker');
        registerHalloPlugin('ultracore-hallofontsize');
        registerHalloPlugin('ultracore-hallofontfamily');
        registerHalloPlugin('ultracore-hallofontcolor');
        </script>
        """
    )


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
    }
