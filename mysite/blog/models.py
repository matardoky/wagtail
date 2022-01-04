from django.db import models
from django import forms 

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField 
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from taggit.models import TaggedItemBase

@register_snippet
class BlogCategory(models.Model):

    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name 

    class Meta:

        verbose_name_plural = 'blog categories'




class BlogIndexPage(Page):

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
  
    
    def get_context(self, request):

        context = super().get_context(request)
        blogpages =  self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context 


class BlogPageTag(TaggedItemBase):

    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_names',
        on_delete=models.CASCADE
    )

class BlogPage(Page):

    date = models.DateField("Post date")
    intro = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
   
   
    def main_image(self):

        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
        MultiFieldPanel([
            FieldPanel('date'), 
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information")
    ]


class BlogPageGalleryImage(Orderable):
    
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=255)

    panels  = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogTagIndexPage(Page): 

    def get_context(self, request):
        tag = request.GET.get('tag') 
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context 



#How to use StreamField for mixed content 

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class PersonBlock(blocks.StructBlock):

    first_name = blocks.CharBlock()
    surname    = blocks.CharBlock()
    photo      = ImageChooserBlock(required=False)
    biography  = blocks.RichTextBlock()
    
    class Meta: 
        icon = 'user'

class NewBlogPage(Page):

    
    author = models.CharField(max_length=255)
    date   = models.DateField("Post date")
    body   = StreamField([
        ('person', PersonBlock()),
        ('heading', blocks.CharBlock(form_classname="full title")), 
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ])
    
    content_panels = Page.content_panels + [
        FieldPanel('author'), 
        FieldPanel('date'), 
        StreamFieldPanel('body')
    ]
