from django.conf.urls import include, url
from . import views

urlpatterns = [
		url(r'^$',views.przepisy),
		url(r'^skladnik/$', views.nowySkladnik, name='skladnik'),
		url(r'^przepis/$', views.nowyPrzepis, name='przepis'),
		url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
		url(r'^detailedsearch_results/$', views.detailed_search), #wyszukiwanie szczegolowe
		url(r'^search_results/$', views.simple_search), #wyszukiwanie zwykle
		url(r'^post/(?P<pk>[0-9]+)/change_ingredients$', views.change_ingredients, name='change_ingredients'),
		url(r'^post/(?P<pk>[0-9]+)/classify$', views.classify, name='classify'),
		url(r'^post/(?P<pk>[0-9]+)/find_similar$', views.find_similar, name='find_similar'),
		url(r'^post/(?P<pk>[0-9]+)/addtag$', views.addtag, name='addtag'),
		]