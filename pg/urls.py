from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from pricegrapher import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pg.views.home', name='home'),
    # url(r'^pg/', include('pg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    url(r'^sandbox/', views.sandbox, name='sandbox'),
    url(r'^$', views.index, name='index'),
    url(r'^lookup/', views.lookup),

    # URLs for product page(s).
    url(r'^products/(?P<pid>\d+)/?$', views.product),
    url(r'^products/(?P<pid>\d+)/([a-z]+)', views.product),
)

