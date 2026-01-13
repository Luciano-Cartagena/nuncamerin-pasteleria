"""
URL configuration for pasteleria project.
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Personalización del admin
admin.site.site_header = "Gestión de Costos - Pastelería"
admin.site.site_title = "Pastelería Admin"
admin.site.index_title = "Panel de Administración"