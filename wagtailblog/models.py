from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    indexed_fields = ('intro', )

    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        # Get blogs
        blogs = self.blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogs, 10)  # Show 10 blogs per page
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
]

BlogIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    body = RichTextField()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    sort_order = models.IntegerField("Sort order", default=0)

    indexed_fields = ('body', )

    class Meta:
        ordering = ['sort_order']

    @property
    def blog_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
]

BlogPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
    FieldPanel('tags'),
    FieldPanel('sort_order'),
]
