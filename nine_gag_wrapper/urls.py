from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'captain_obvious.views.index'),
    url(r'^gag/(?P<gag_id>\d+)$', 'captain_obvious.views.index'),
    url(r'^mc/$', 'captain_obvious.views.meme_class'),
    url(r'^graph/comment/$', 'captain_obvious.views.graph_comment'),
    # url(r'^nine_gag_wrapper/', include('nine_gag_wrapper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
