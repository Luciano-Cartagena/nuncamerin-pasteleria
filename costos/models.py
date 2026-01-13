from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class Ingrediente(models.Model):
    """
    Modelo para almacenar información de ingredientes.
    
    Decisiones técnicas:
    - Uso Decimal para precios para evitar errores de redondeo
    - CharField para unidades con choices predefinidas
    - auto_now para fecha de actualización automática
    """
    
    UNIDADES_CHOICES = [
        ('g', 'Gramos'),
        ('ml', 'Mililitros'),
        ('unidad', 'Unidad'),
        ('kg', 'Kilogramos'),
        ('l', 'Litros'),
    ]
    
    nombre = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Nombre del ingrediente (ej: Harina 0000)"
    )
    precio_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Precio por unidad base"
    )
    unidad_base = models.CharField(
        max_length=10, 
        choices=UNIDADES_CHOICES,
        help_text="Unidad de medida base para el precio"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Última actualización del precio"
    )
    
    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} (${self.precio_base}/{self.unidad_base})"
    
    def precio_por_gramo(self):
        """
        Calcula el precio por gramo del ingrediente.
        Convierte todas las unidades a gramos para cálculos uniformes.
        """
        if self.unidad_base == 'g':
            return self.precio_base
        elif self.unidad_base == 'kg':
            return self.precio_base / 1000
        elif self.unidad_base == 'ml':
            # Asumimos densidad 1 (1ml = 1g) para líquidos
            return self.precio_base
        elif self.unidad_base == 'l':
            return self.precio_base / 1000
        elif self.unidad_base == 'unidad':
            # Para unidades, retornamos el precio base
            return self.precio_base
        return self.precio_base


class Receta(models.Model):
    """
    Modelo para las recetas/productos de la pastelería.
    
    Decisiones técnicas:
    - Relación ManyToMany con Ingrediente a través de IngredienteReceta
    - Margen de ganancia como DecimalField con validación
    - Métodos para cálculo automático de costos
    """
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del producto/postre"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción opcional del producto"
    )
    margen_ganancia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('50.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Margen de ganancia en porcentaje (ej: 50.00 para 50%)"
    )
    ingredientes = models.ManyToManyField(
        Ingrediente,
        through='IngredienteReceta',
        help_text="Ingredientes que componen esta receta"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def costo_total(self):
        """
        Calcula el costo total de la receta sumando todos los ingredientes.
        """
        total = Decimal('0.00')
        for ingrediente_receta in self.ingredientereceta_set.all():
            total += ingrediente_receta.costo_ingrediente()
        return total
    
    def precio_sugerido(self):
        """
        Calcula el precio de venta sugerido aplicando el margen de ganancia.
        Fórmula: costo_total * (1 + margen_ganancia/100)
        """
        costo = self.costo_total()
        if costo > 0:
            return costo * (1 + self.margen_ganancia / 100)
        return Decimal('0.00')


class IngredienteReceta(models.Model):
    """
    Modelo intermedio para la relación ManyToMany entre Receta e Ingrediente.
    Almacena la cantidad específica de cada ingrediente en cada receta.
    
    Decisiones técnicas:
    - Cantidad como DecimalField para precisión
    - Unidad de medida para flexibilidad
    - Método para calcular costo específico
    """
    
    UNIDADES_CHOICES = [
        ('g', 'Gramos'),
        ('ml', 'Mililitros'),
        ('unidad', 'Unidad'),
        ('kg', 'Kilogramos'),
        ('l', 'Litros'),
    ]
    
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        help_text="Cantidad del ingrediente necesaria"
    )
    unidad = models.CharField(
        max_length=10,
        choices=UNIDADES_CHOICES,
        help_text="Unidad de medida para esta cantidad"
    )
    
    class Meta:
        verbose_name = "Ingrediente de Receta"
        verbose_name_plural = "Ingredientes de Receta"
        unique_together = ['receta', 'ingrediente']
    
    def __str__(self):
        return f"{self.receta.nombre} - {self.ingrediente.nombre} ({self.cantidad} {self.unidad})"
    
    def costo_ingrediente(self):
        """
        Calcula el costo de este ingrediente específico en la receta.
        Convierte las unidades según sea necesario.
        """
        # Convertir cantidad a gramos para cálculo uniforme
        cantidad_en_gramos = self._convertir_a_gramos()
        
        if self.ingrediente.unidad_base == 'unidad' and self.unidad == 'unidad':
            # Para ingredientes por unidad, multiplicar directamente
            return self.ingrediente.precio_base * self.cantidad
        else:
            # Para ingredientes por peso/volumen, usar precio por gramo
            precio_por_gramo = self.ingrediente.precio_por_gramo()
            return precio_por_gramo * cantidad_en_gramos
    
    def _convertir_a_gramos(self):
        """
        Convierte la cantidad a gramos para cálculos uniformes.
        """
        if self.unidad == 'g':
            return self.cantidad
        elif self.unidad == 'kg':
            return self.cantidad * 1000
        elif self.unidad == 'ml':
            # Asumimos densidad 1 para líquidos
            return self.cantidad
        elif self.unidad == 'l':
            return self.cantidad * 1000
        elif self.unidad == 'unidad':
            return self.cantidad
        return self.cantidad