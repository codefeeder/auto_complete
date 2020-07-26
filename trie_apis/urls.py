from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.cache import cache_page
from . import views


urlpatterns = [
    re_path(r'^query$', cache_page(3)(views.search)),
    path('add', views.add),
    path('delete', views.delete_location),
    path('add/', views.add),
    path('delete/', views.delete_location),
    path('modify', views.change_popularity),
    path('modify/', views.change_popularity),
]

urlpatterns = format_suffix_patterns(urlpatterns)
