from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'captain_obvious.views.index'),
    url(r'^gag/(?P<gag_id>\d+)$', 'captain_obvious.views.index'),
    url(r'^mc/$', 'captain_obvious.views.meme_class'),
    url(r'^9gag/post/$', 'captain_obvious.views.nine_gag_post'),
    url(r'^graph/comments/$', 'captain_obvious.views.graph_comments'),
    url(r'^graph/user/$', 'captain_obvious.views.graph_user'),

    url(r'^lookup/recomm/(?P<gag_id>\d+)$', 'crowd_lookup.views.get_recomm_words'),
    url(r'^lookup/query/$', 'crowd_lookup.views.query_word'),
    # url(r'^nine_gag_wrapper/', include('nine_gag_wrapper.foo.urls')),

    url(r'^lookup/recomm/(?P<gag_id>\d+)$', 'crowd_lookup.views.get_recomm_words'),
    url(r'^lookup/query/(?P<gag_id>\d+)$', 'crowd_lookup.views.query_word'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
