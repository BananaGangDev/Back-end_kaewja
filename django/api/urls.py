from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('', include('login.urls')),
    path('', include('concordancer.urls')),
    path('', include('error_tagger.urls')),
    path('', include('tagset.urls'))
]
