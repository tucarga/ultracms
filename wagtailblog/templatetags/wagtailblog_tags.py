from django import template

from wagtailblog.models import BlogPage, BlogIndexPage

register = template.Library()


@register.inclusion_tag(
    'wagtailblog/tags/blog_listing_homepage.html',
    takes_context=True
)
def blog_listing_homepage(context, count=2):
    blogs = BlogPage.objects.filter(live=True).order_by('-date')
    return {
        'blogs': blogs[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag(
    'wagtailblog/tags/blog_index_homepage.html',
    takes_context=True
)
def blog_index(context, title):
    blog_index = BlogIndexPage.objects.get(title=title, live=True)
    # import pdb; pdb.set_trace()
    return {
        'blog_index': blog_index,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
