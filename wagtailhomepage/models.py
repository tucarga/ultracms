from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin import edit_handlers
from wagtail.wagtailcore import fields
from wagtail.wagtailcore import models as wagtail_models

from ultracore.models import CarouselItem


class HomePageCarouselItem(wagtail_models.Orderable, CarouselItem):
    page = ParentalKey('wagtailhomepage.HomePage',
                       related_name='carousel_items')


class HomePage(wagtail_models.Page):

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    edit_handlers.FieldPanel('title', classname="full title"),
    edit_handlers.InlinePanel(
        HomePage, 'carousel_items', label="Carousel items"),
]

HomePage.promote_panels = [
    edit_handlers.MultiFieldPanel(
        wagtail_models.Page.promote_panels, "Common page configuration"),
]
