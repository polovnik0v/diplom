from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pvz_app.urls')), 
    path('admin/', admin.site.urls),
    path('pvz/', include('pvz_app.urls')),
]
