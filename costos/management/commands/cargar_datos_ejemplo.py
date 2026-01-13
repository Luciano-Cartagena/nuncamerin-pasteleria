from django.core.management.base import BaseCommand
from decimal import Decimal
from costos.models import Ingrediente, Receta, IngredienteReceta


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para la pastelería'

    def handle(self, *args, **options):
        self.stdout.write('Cargando ingredientes de ejemplo...')
        
        # Crear ingredientes básicos
        ingredientes_data = [
            # Harinas
            ('Harina 0000', Decimal('180.00'), 'kg'),
            ('Harina Leudante', Decimal('200.00'), 'kg'),
            ('Harina Integral', Decimal('220.00'), 'kg'),
            
            # Azúcares
            ('Azúcar Común', Decimal('150.00'), 'kg'),
            ('Azúcar Impalpable', Decimal('280.00'), 'kg'),
            ('Azúcar Rubia', Decimal('200.00'), 'kg'),
            
            # Lácteos
            ('Leche Entera', Decimal('120.00'), 'l'),
            ('Crema de Leche', Decimal('350.00'), 'l'),
            ('Manteca', Decimal('450.00'), 'kg'),
            ('Queso Crema', Decimal('800.00'), 'kg'),
            
            # Huevos y otros
            ('Huevo', Decimal('30.00'), 'unidad'),
            ('Vainilla', Decimal('15.00'), 'ml'),
            ('Polvo de Hornear', Decimal('8.00'), 'g'),
            ('Sal', Decimal('2.00'), 'g'),
            
            # Chocolates
            ('Chocolate Semi-amargo', Decimal('1200.00'), 'kg'),
            ('Cacao en Polvo', Decimal('800.00'), 'kg'),
            ('Dulce de Leche', Decimal('600.00'), 'kg'),
            
            # Frutas
            ('Limón', Decimal('80.00'), 'unidad'),
            ('Naranja', Decimal('60.00'), 'unidad'),
        ]
        
        ingredientes_creados = []
        for nombre, precio, unidad in ingredientes_data:
            ingrediente, created = Ingrediente.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'precio_base': precio,
                    'unidad_base': unidad
                }
            )
            if created:
                ingredientes_creados.append(ingrediente)
                self.stdout.write(f'  ✓ {nombre}')
        
        self.stdout.write(f'Ingredientes creados: {len(ingredientes_creados)}')
        
        # Crear recetas de ejemplo
        self.stdout.write('\nCreando recetas de ejemplo...')
        
        # Torta de Vainilla
        torta_vainilla, created = Receta.objects.get_or_create(
            nombre="Torta de Vainilla",
            defaults={
                'descripcion': 'Torta clásica de vainilla esponjosa',
                'margen_ganancia': Decimal('60.00')
            }
        )
        
        if created:
            # Ingredientes para torta de vainilla
            ingredientes_torta = [
                ('Harina 0000', Decimal('300'), 'g'),
                ('Azúcar Común', Decimal('250'), 'g'),
                ('Huevo', Decimal('3'), 'unidad'),
                ('Manteca', Decimal('150'), 'g'),
                ('Leche Entera', Decimal('200'), 'ml'),
                ('Polvo de Hornear', Decimal('10'), 'g'),
                ('Vainilla', Decimal('5'), 'ml'),
                ('Sal', Decimal('2'), 'g'),
            ]
            
            for nombre_ing, cantidad, unidad in ingredientes_torta:
                ingrediente = Ingrediente.objects.get(nombre=nombre_ing)
                IngredienteReceta.objects.create(
                    receta=torta_vainilla,
                    ingrediente=ingrediente,
                    cantidad=cantidad,
                    unidad=unidad
                )
            
            self.stdout.write('  ✓ Torta de Vainilla')
        
        # Brownie de Chocolate
        brownie, created = Receta.objects.get_or_create(
            nombre="Brownie de Chocolate",
            defaults={
                'descripcion': 'Brownie húmedo con chocolate semi-amargo',
                'margen_ganancia': Decimal('70.00')
            }
        )
        
        if created:
            ingredientes_brownie = [
                ('Chocolate Semi-amargo', Decimal('200'), 'g'),
                ('Manteca', Decimal('150'), 'g'),
                ('Azúcar Común', Decimal('200'), 'g'),
                ('Huevo', Decimal('3'), 'unidad'),
                ('Harina 0000', Decimal('100'), 'g'),
                ('Cacao en Polvo', Decimal('30'), 'g'),
                ('Sal', Decimal('2'), 'g'),
            ]
            
            for nombre_ing, cantidad, unidad in ingredientes_brownie:
                ingrediente = Ingrediente.objects.get(nombre=nombre_ing)
                IngredienteReceta.objects.create(
                    receta=brownie,
                    ingrediente=ingrediente,
                    cantidad=cantidad,
                    unidad=unidad
                )
            
            self.stdout.write('  ✓ Brownie de Chocolate')
        
        # Cheesecake
        cheesecake, created = Receta.objects.get_or_create(
            nombre="Cheesecake Clásico",
            defaults={
                'descripcion': 'Cheesecake cremoso con base de galletas',
                'margen_ganancia': Decimal('80.00')
            }
        )
        
        if created:
            ingredientes_cheesecake = [
                ('Queso Crema', Decimal('500'), 'g'),
                ('Azúcar Común', Decimal('150'), 'g'),
                ('Huevo', Decimal('3'), 'unidad'),
                ('Crema de Leche', Decimal('200'), 'ml'),
                ('Vainilla', Decimal('5'), 'ml'),
            ]
            
            for nombre_ing, cantidad, unidad in ingredientes_cheesecake:
                ingrediente = Ingrediente.objects.get(nombre=nombre_ing)
                IngredienteReceta.objects.create(
                    receta=cheesecake,
                    ingrediente=ingrediente,
                    cantidad=cantidad,
                    unidad=unidad
                )
            
            self.stdout.write('  ✓ Cheesecake Clásico')
        
        self.stdout.write(self.style.SUCCESS('\n¡Datos de ejemplo cargados exitosamente!'))
        self.stdout.write('\nPuedes acceder al admin en: http://127.0.0.1:8000/admin/')
        self.stdout.write('Recuerda crear un superusuario con: python manage.py createsuperuser')