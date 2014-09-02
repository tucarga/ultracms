from django.db import models

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


class HomePage(wagtail_models.Page):

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
]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPageTag(TaggedItemBase):
    content_object = ParentalKey('ultracore.FormPage',
                                 related_name='tagged_items')


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    tags = ClusterTaggableManager(through=FormPageTag, blank=True)


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
    ]


class StandardPage(wagtail_models.Page):
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
]


class SpecialPageTag(TaggedItemBase):
    content_object = ParentalKey('ultracore.SpecialPage',
                                 related_name='tagged_items')


class SpecialPage(wagtail_models.Page):
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
]


class DirectoryPage(wagtail_models.Page):
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
]


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    tags = models.ManyToManyField('taggit.Tag', blank=True)

    panels = [
        FieldPanel('full_name'),
        FieldPanel('position'),
        FieldPanel('phone'),
        FieldPanel('email'),
        FieldPanel('tags'),
    ]

#     def save(self, *args, **kwargs):
#         import pdb; pdb.set_trace()

    def __unicode__(self):
        return self.full_name

register_snippet(Contact)

from taggit.models import Tag

Tag.panels = [
    FieldPanel('name'),
]


register_snippet(Tag)

# Settings

@register_setting
class SiteSetting(BaseSetting):
    title = models.CharField(max_length=255)
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    footer = RichTextField()

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('site_logo'),
        ImageChooserPanel('background_image'),
        FieldPanel('footer'),
    ]


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
