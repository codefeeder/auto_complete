from django.contrib import admin
from django.urls import include, path, re_path
from .views import login


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('trie_apis.urls')),
    path('api/login', login)
]
