from django.conf.urls import *

urlpatterns = patterns('home.views',
   url(r'^$', 'index', name="index"),
   url(r'^xem-nhieu/$', 'index', {'views': 'xem-nhieu'}),
   url(r'^binh-luan-nhieu/$', 'index', {'views': 'binh-luan-nhieu'}),
   url(r'^most-view/$', 'index', {'views': 'xem-nhieu'}),
   url(r'^most-comment/$', 'index', {'views': 'binh-luan-nhieu'}),
   url(r'^get-posts/$', 'get_posts'),
   url(r'^get-more-images/$', 'get_images_more'),
   url(r'^commented/$', 'commented'),
   url(r'^liked/$', 'liked'),
   url(r'^get-images/$', 'get_images'),
   url(r'^upload-image/$', 'upload_image'),
   url(r'^get-posts-detail-more/$', 'get_posts_detail_more'),
   url(r'^relative-post/(?P<category>[-\w]+)/$', 'category_post_relative', name='list_post_relative_category'),
   url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', 'detail_post', name="detail_post"),
   url(r'^(?P<category>[-\w]+)/$', 'category', name='list_post_category'),
)
