from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('southindiancoffee/api-admin/', admin.site.urls),
    path('v1/', include('core.urls')),
    path('api-docs/', include_docs_urls(title='South Indian Coffee V1 APIs')),
]
