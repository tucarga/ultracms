from wagtail.wagtailcore import models as wagtail_models
from wagtail.wagtailcore import fields
from wagtail.wagtailadmin import edit_handlers


class HomePage(wagtail_models.Page):
    body = fields.RichTextField(blank=True)

    indexed_fields = ('body', )

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    edit_handlers.FieldPanel('title', classname="full title"),
    edit_handlers.FieldPanel('body', classname="full"),
    # edit_handlers.InlinePanel(
    #     HomePage, 'carousel_items', label="Carousel items"),
    # edit_handlers.InlinePanel(
    #     HomePage, 'related_links', label="Related links"),
]

HomePage.promote_panels = [
    edit_handlers.MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
]
