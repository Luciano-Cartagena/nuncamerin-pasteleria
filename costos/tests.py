from django.test import TestCase
from decimal import Decimal
from .models import Ingrediente, Receta, IngredienteReceta


class IngredienteTestCase(TestCase):
    """Tests para el modelo Ingrediente."""
    
    def setUp(self):
        self.harina = Ingrediente.objects.create(
            nombre="Harina 0000",
            precio_base=Decimal('150.00'),
            unidad_base='kg'
        )
        self.huevo = Ingrediente.objects.create(
            nombre="Huevo",
            precio_base=Decimal('25.00'),
            unidad_base='unidad'
        )
    
    def test_precio_por_gramo_kg(self):
        """Test conversión de kg a gramos."""
        precio_gramo = self.harina.precio_por_gramo()
        self.assertEqual(precio_gramo, Decimal('0.15'))  # 150/1000
    
    def test_precio_por_gramo_unidad(self):
        """Test precio por unidad."""
        precio_unidad = self.huevo.precio_por_gramo()
        self.assertEqual(precio_unidad, Decimal('25.00'))


class RecetaTestCase(TestCase):
    """Tests para el modelo Receta y cálculos."""
    
    def setUp(self):
        # Crear ingredientes
        self.harina = Ingrediente.objects.create(
            nombre="Harina 0000",
            precio_base=Decimal('150.00'),
            unidad_base='kg'
        )
        self.azucar = Ingrediente.objects.create(
            nombre="Azúcar",
            precio_base=Decimal('120.00'),
            unidad_base='kg'
        )
        
        # Crear receta
        self.torta = Receta.objects.create(
            nombre="Torta de Vainilla",
            margen_ganancia=Decimal('50.00')
        )
        
        # Agregar ingredientes a la receta
        IngredienteReceta.objects.create(
            receta=self.torta,
            ingrediente=self.harina,
            cantidad=Decimal('500'),  # 500g
            unidad='g'
        )
        IngredienteReceta.objects.create(
            receta=self.torta,
            ingrediente=self.azucar,
            cantidad=Decimal('300'),  # 300g
            unidad='g'
        )
    
    def test_costo_total_receta(self):
        """Test cálculo del costo total de una receta."""
        # Harina: 500g * 0.15 = 75
        # Azúcar: 300g * 0.12 = 36
        # Total: 111
        costo_esperado = Decimal('111.00')
        self.assertEqual(self.torta.costo_total(), costo_esperado)
    
    def test_precio_sugerido(self):
        """Test cálculo del precio sugerido con margen."""
        # Costo: 111, Margen: 50%
        # Precio: 111 * 1.5 = 166.5
        precio_esperado = Decimal('166.50')
        self.assertEqual(self.torta.precio_sugerido(), precio_esperado)