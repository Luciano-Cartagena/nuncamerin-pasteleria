from django.contrib import admin
from .models import Ingrediente, Receta, IngredienteReceta


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    """Admin simplificado para Ingredientes."""
    
    list_display = ['nombre', 'precio_base', 'unidad_base', 'fecha_actualizacion']
    list_filter = ['unidad_base', 'fecha_actualizacion']
    search_fields = ['nombre']
    readonly_fields = ['fecha_actualizacion']


class IngredienteRecetaInline(admin.TabularInline):
    """Inline simplificado para ingredientes en recetas."""
    
    model = IngredienteReceta
    extra = 1
    fields = ['ingrediente', 'cantidad', 'unidad']


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    """Admin simplificado para Recetas."""
    
    list_display = ['nombre', 'margen_ganancia', 'fecha_modificacion']
    list_filter = ['fecha_creacion', 'fecha_modificacion']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    fields = ['nombre', 'descripcion', 'margen_ganancia', 'fecha_creacion', 'fecha_modificacion']
    inlines = [IngredienteRecetaInline]


@admin.register(IngredienteReceta)
class IngredienteRecetaAdmin(admin.ModelAdmin):
    """Admin simplificado para relaciones ingrediente-receta."""
    
    list_display = ['receta', 'ingrediente', 'cantidad', 'unidad']
    list_filter = ['receta', 'ingrediente', 'unidad']
    search_fields = ['receta__nombre', 'ingrediente__nombre']