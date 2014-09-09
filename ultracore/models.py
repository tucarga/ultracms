from django.db import models
from pygal.colors import darken, lighten

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel
from wagtail.wagtailcore import models as wagtail_models
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from wagtailsettings.models import register_setting, BaseSetting


COLOR_CHOICES = (
    ('#000000', "Black"),
    ('#7bd148', "Green"),
    ('#5484ed', "Bold blue"),
    ('#a4bdfc', "Blue"),
    ('#46d6db', "Turquoise"),
    ('#7ae7bf', "Light green"),
    ('#51b749', "Bold green"),
    ('#fbd75b', "Yellow"),
    ('#ffb878', "Orange"),
    ('#ff887c', "Red"),
    ('#dc2127', "Bold red"),
    ('#dbadff', "Purple"),
    ('#e1e1e1', "Gray"),
)
FONT_SIZE_DEFAULT = 10
COLOR_FIELD_DEFAULT_MAX_LENGTH = len(COLOR_CHOICES[0][0])
COLOR_DARKEN_DEFAULT_PERCENTAGE = 10
COLOR_LIGHTEN_DEFAULT_PERCENTAGE = 10


class AbstractPageExtension(models.Model):
    background_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)

    class Meta:
        abstract = True


AbstractPageExtension.promote_panels = [FieldPanel('background_color')]


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class HomePageCarouselItem(wagtail_models.Orderable, CarouselItem):
    page = ParentalKey('ultracore.HomePage',
                       related_name='carousel_items')


class Service(LinkFields):
    title = models.CharField(max_length=255)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('feed_image'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __unicode__(self):
        return self.title


class HomePageService(wagtail_models.Orderable, Service):
    page = ParentalKey('ultracore.HomePage',
                       related_name='services')


class HomePage(wagtail_models.Page, AbstractPageExtension):

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    InlinePanel(
        HomePage, 'carousel_items', label="Carousel items"),
    InlinePanel(
        HomePage, 'services', label="Services"),
]

HomePage.promote_panels = [
    MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
] + AbstractPageExtension.promote_panels


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPageTag(TaggedItemBase):
    content_object = ParentalKey('ultracore.FormPage',
                                 related_name='tagged_items')


class FormPage(AbstractEmailForm, AbstractPageExtension):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    tags = ClusterTaggableManager(through=FormPageTag, blank=True)

    # style
    font_size = models.IntegerField(default=FONT_SIZE_DEFAULT)
    font_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)
    button_text = models.CharField(max_length=30)

FormPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(FormPage, 'form_fields', label="Form fields"),
    FieldPanel('thank_you_text', classname="full"),
    MultiFieldPanel([
        FieldPanel('to_address', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('subject', classname="full"),
    ], "Email")
]

FormPage.promote_panels = [
    MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
    FieldPanel('tags'),
    MultiFieldPanel([
        FieldPanel('font_size'),
        FieldPanel('font_color'),
        FieldPanel('button_text'), ] + AbstractPageExtension.promote_panels,
        "Style")
]


class StandardPage(wagtail_models.Page, AbstractPageExtension):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )

    hide_link_in_menu = models.BooleanField()

    class Meta:
        verbose_name = "StandardPage"

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]

StandardPage.promote_panels = [
    MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
    FieldPanel('hide_link_in_menu'),
] + AbstractPageExtension.promote_panels


class SpecialPageTag(TaggedItemBase):
    content_object = ParentalKey('ultracore.SpecialPage',
                                 related_name='tagged_items')


class SpecialPage(wagtail_models.Page, AbstractPageExtension):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    side_title = RichTextField(blank=True)
    body = RichTextField(blank=True)

    tags = ClusterTaggableManager(through=SpecialPageTag, blank=True)

    hide_link_in_menu = models.BooleanField()

    indexed_fields = ('body', )

    class Meta:
        verbose_name = "SpecialPage"

SpecialPage.content_panels = [
    ImageChooserPanel('feed_image'),
    FieldPanel('title', classname="full title"),
    FieldPanel('side_title', classname="full"),
    FieldPanel('body', classname="full"),
]

SpecialPage.promote_panels = [
    MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
    FieldPanel('tags'),
    FieldPanel('hide_link_in_menu'),
] + AbstractPageExtension.promote_panels


class DirectoryPage(wagtail_models.Page, AbstractPageExtension):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )

    hide_link_in_menu = models.BooleanField()

    class Meta:
        verbose_name = "DirectoryPage"

DirectoryPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]

DirectoryPage.promote_panels = [
    MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
    FieldPanel('hide_link_in_menu'),
] + AbstractPageExtension.promote_panels


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    area = models.ForeignKey('Area')
    agency = models.ForeignKey('Agency')

    tags = models.ManyToManyField('taggit.Tag', blank=True)

    panels = [
        FieldPanel('full_name'),
        FieldPanel('position'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('area'),
        FieldPanel('agency'),

        FieldPanel('tags'),
    ]

    class Meta:
        ordering = ('full_name', )

    def __unicode__(self):
        return self.full_name

register_snippet(Contact)


class Area(models.Model):
    name = models.CharField(max_length=100)
    content = RichTextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('content', classname="full"),
    ]

    def __unicode__(self):
        return self.name

register_snippet(Area)


class Agency(models.Model):
    name = models.CharField(max_length=100)
    content = RichTextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('content', classname="full"),
    ]

    class Meta:
        verbose_name = "Agencies"

    def __unicode__(self):
        return self.name

register_snippet(Agency)


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('link', classname="full"),
    ]

    def __unicode__(self):
        return self.name

register_snippet(MenuItem)


from taggit.models import Tag

Tag.panels = [
    FieldPanel('name'),
]


register_snippet(Tag)

# Settings


@register_setting
class SiteSetting(BaseSetting):
    title = models.CharField(max_length=255)
    site_logo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    background_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    background_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)
    footer = RichTextField(null=True, blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            ImageChooserPanel('site_logo'),
            ImageChooserPanel('background_image'),
            FieldPanel('background_color'),
            FieldPanel('content_background_color'), ],
            "Content"),
        MultiFieldPanel([
            FieldPanel('header_background_color'),
            FieldPanel('header_menu_parent_background_color'),
            FieldPanel('header_font_size'),
            FieldPanel('header_font_color'),
            FieldPanel('header_font_color_hover'), ],
            "Header"),
        MultiFieldPanel([
            FieldPanel('secondary_menu_font_size'),
            FieldPanel('secondary_menu_font_color'),
            FieldPanel('secondary_menu_font_color_hover'), ],
            "Secondary menu"),
        MultiFieldPanel([
            FieldPanel('contacts_menu_font_size'),
            FieldPanel('contacts_menu_font_color'), ],
            "Contacts menu"),
        MultiFieldPanel([
            FieldPanel('footer'),
            FieldPanel('footer_background_color'), ],
            "Footer"),
        MultiFieldPanel([
            FieldPanel('google_analytics_code'), ],
            "Google Analytics"),
    ]

    # secondary menu settings
    secondary_menu_font_size = models.IntegerField(null=True, blank=True)
    secondary_menu_font_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)
    secondary_menu_font_color_hover = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)

    # contact settings
    contacts_menu_font_size = models.IntegerField(null=True, blank=True)
    contacts_menu_font_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)

    # google analytics
    google_analytics_code = models.CharField(max_length=13, null=True, blank=True)

    # header
    header_background_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)
    header_menu_parent_background_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)
    header_font_size = models.IntegerField(null=True, blank=True)
    header_font_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)
    header_font_color_hover = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)

    # content
    content_background_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)

    # footer
    footer_background_color = models.CharField(max_length=COLOR_FIELD_DEFAULT_MAX_LENGTH, choices=COLOR_CHOICES, null=True, blank=True)

    @property
    def header_font_color_active(self):
        return self.header_font_color

    @property
    def header_menu_parent_background_color_hover(self):
        return darken(self.header_menu_parent_background_color, COLOR_DARKEN_DEFAULT_PERCENTAGE)

    @property
    def header_menu_parent_background_color_active(self):
        return darken(self.header_menu_parent_background_color, COLOR_DARKEN_DEFAULT_PERCENTAGE)

    @property
    def header_menu_children_background_color(self):
        return lighten(self.header_menu_parent_background_color, COLOR_LIGHTEN_DEFAULT_PERCENTAGE)

    @property
    def header_menu_children_background_color_hover(self):
        return self.header_menu_parent_background_color

# This is required only if no method is found to have auto complete
# tags in models that have a `tags` field like `SpecialPage`.
#
#    HACK -- MONKEY PATCH TO HIDE THE HIDDEN FIELDS THAT CANNOT BE EXCLUDED
#
# from https://github.com/torchbox/wagtail/issues/338


from wagtail.wagtailadmin.edit_handlers import WagtailAdminModelForm
WagtailAdminModelFormInit = WagtailAdminModelForm.__init__


def PatchedWagtailAdminModelFormInit(self, *args, **kwargs):
    WagtailAdminModelFormInit(self, *args, **kwargs)

    from django import forms

    HIDDEN_FIELDS = ['slug']

    if isinstance(self.instance, Tag):
        for field_name in HIDDEN_FIELDS:
            self.fields[field_name].required = False
            self.fields[field_name].widget = forms.HiddenInput()

WagtailAdminModelForm.__init__ = PatchedWagtailAdminModelFormInit
#
#    END HACK
#
