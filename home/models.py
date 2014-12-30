from django.db import models
from django.contrib.auth.models import User
import pytz
from pytz import timezone
import datetime
from django.core.paginator import Paginator, PageNotAnInteger

from django.template.defaultfilters import slugify
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from django.core.cache import cache

from google.appengine.api import images

from tinymce.models import HTMLField

class UtcTzinfo(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def olsen_name(self):
        return 'UTC'


TZINFOS = {
    'utc': UtcTzinfo(),
}



class Category(models.Model):
    name = models.CharField(max_length=135, unique=True, null=True)#HTMLField()
    name_en = models.CharField(max_length=135, null=True, blank=True)
    slug = models.SlugField(blank=False, max_length=255, unique=True)
    slug_en = models.SlugField(blank=False, max_length=255, unique=True)
    parent_id = models.ForeignKey('self', null=True, blank=True)
    order = models.IntegerField(default=0)
    image_url = models.CharField( max_length=500, null=True,  blank=True)

    def as_dict(self):
        return {
            "name": self.name,
            "image":self.image_url,
            "url": self.get_absolute_url(),
            "views":self.count_views(),
            "posts":self.count_post(),
        }

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("list_post_category", [self.slug])

    @staticmethod
    def get_category(self, category_id=None):
        categories = Category.objects.filter(parent_id=category_id)
        return categories

    def count_post(self):
        return POST.objects.filter(category=self).count()

    def count_views(self):
        return sum((x.views for x in POST.objects.filter(category=self)))

    def image_tag(self):
        return '<img src="%s=s100" />' % self.image_url

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.name_en is None:
            self.slug_en = slugify(self.name)
        else:
            self.slug_en = slugify(self.name_en)
        if memcache.get('categories-vi') is not None:
            memcache.delete('categories-vi')
        if memcache.get('categories-en') is not None:
            memcache.delete('categories-en')
        cache.clear()
        super(Category, self).save(*args, **kwargs)

class IMAGE_STORE(models.Model):
    blob_key = models.CharField(max_length=500,  null=True)
    file_name = models.CharField(max_length=235, null=True)
    size = models.IntegerField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u"%s" % self.file_name

    def image_tag(self):
        return u'<img src="%s=s100" />' % images.get_serving_url(self.blob_key)

    def delete(self, *args, **kwargs):
        blobstore.delete(self.blob_key)
        super(IMAGE_STORE, self).delete(*args, **kwargs)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class POST(models.Model):
    category = models.ForeignKey(Category, null=False, related_name='page_category')
    author = models.ForeignKey(User)
    title = models.CharField(max_length=235, unique=True, null=True)
    slug = models.SlugField(blank=False, max_length=255, unique=True)
    description = models.TextField()
    link = models.TextField(null=True,blank=True)
    typePost = models.TextField(default="text")
    content = HTMLField()
    views = models.IntegerField(null=True,blank=True,default=0)
    likes = models.IntegerField(null=True,blank=True,default=0)
    comments = models.IntegerField(null=True,blank=True,default=0)
    start = models.IntegerField(null=True,blank=True,default=0)
    end = models.IntegerField(null=True,blank=True,default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ("detail_post", [self.category.slug,self.slug])

    @property
    def is_past_due(self):
        if datetime.date.today() > self.date:
            return True
        return False

    def updateView(self):
        if self.views is None:
            self.views = 1
        else:
            self.views = self.views + 1
        self.save()

    def updateComment(self, typePost=None):
        if self.comments is None and typePost is None:
            self.comments = 1
        elif self.comments is not None and typePost is not None :
            self.comments = self.comments - 1
        elif self.comments is not None and typePost is None:
            self.comments = self.comments + 1
        self.save()

    def updateLike(self, typePost=None):
        if self.likes is None and typePost is None:
            self.likes = 1
        elif self.likes is not None and typePost is not None :
            self.likes = self.likes - 1
        elif self.likes is not None and typePost is None:
            self.likes = self.likes + 1
        self.save()
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.typePost != "text":
            self.link = self.link.replace("https://www.youtube.com/watch?v=", "")
        if memcache.get('post-trang-chu') is not None:
            memcache.delete('post-trang-chu')

        if memcache.get(self.category.slug) is not None:
            memcache.delete(self.category.slug)

        self.expire_view_cache("index")
        self.expire_view_cache("category")
        cache.clear()
            
        super(POST, self).save(*args, **kwargs)


    def expire_view_cache(view_name, args=[], namespace=None, key_prefix=None):
        """
        This function allows you to invalidate any view-level cache. 
            view_name: view function you wish to invalidate or it's named url pattern
            args: any arguments passed to the view function
            namepace: optioal, if an application namespace is needed
            key prefix: for the @cache_page decorator for the function (if any)
        """
        from django.core.urlresolvers import reverse
        from django.http import HttpRequest
        from django.utils.cache import get_cache_key
        from django.core.cache import cache
        # create a fake request object
        request = HttpRequest()
        # Loookup the request path:
        if namespace:
            view_name = namespace + ":" + view_name
        request.path = view_name#reverse(view_name, args=args)
        # get cache key, expire if the cached item exists:
        key = get_cache_key(request, key_prefix=key_prefix)
        if key:
            if cache.get(key):
                cache.delete(key)
            return True
        return False


    def translate(self):
        utc = TZINFOS['utc']
        self.date = self.date.replace(tzinfo=utc)
        return self.date.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))